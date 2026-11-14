import os
import uuid
import logging
from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError

from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from common.mixins import SearchMixin
from common.models.other import Sherkat
from common.pagination import CustomPagination
from contracts.models.models import (
    Contract,
    ContractDomin,
    ContractElhaghye,
    ShrhCatalog,
    ShrhContract,
)
from initialborders.models.models import InitialBorder, ContractInitialBorder, InitialBorderDomin
from logs.utils import get_details_from_request

delete_logger = logging.getLogger("delete_activity_logger")
api_activity_logger = logging.getLogger("api_activity_logger")



class ContractListApiViews(SearchMixin, APIView):
    """
    GET: list of contracts (superuser: all, others: only the ones they have access to)

    POST (application/json): create a contract together with its initial borders
    and its shrh items (selected from ShrhCatalog).
        - initborder_ids   : ids of already existing initial borders
                             (must not be linked to another contract that is still active,
                             i.e. not completed and its end_date not passed).
                             At least one is required.
        - shrh_items       : (optional) list of objects, each one becomes a ShrhContract row:
                               {"shrh_catalog": <id>, "scale": <int|null>,
                                "percentage": <0-100>, "worked_percentage": <0-100>}
                             Every shrh_catalog must be a non-group item whose `contract_domin`
                             is the same as the contract's `dtyp`. The same catalog item may be
                             repeated only with different scales (at most once without scale).
        - moshaver_arshad  : (optional) id of a Sherkat that is allowed to be moshaver arshad.
        Everything is created in ONE transaction: if any part fails, nothing is saved.
    """

    search_fields = ["title", "dtyp__title", "number"]

    class ContractListOutputSerializer(serializers.ModelSerializer):
        class ContractListOutputSerializerDtyp(serializers.ModelSerializer):
            class Meta:
                model = ContractDomin
                fields = ["id", "title", "code"]

        class ContractListOutputSerializerInitborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ["id", "title"]

        class ContractListOutputSerializerMoshaverArshad(serializers.ModelSerializer):
            class Meta:
                model = Sherkat
                fields = ["id", "name", "typ", "code"]

        dtyp = ContractListOutputSerializerDtyp()
        initborders = ContractListOutputSerializerInitborder(many=True)
        moshaver_arshad = ContractListOutputSerializerMoshaverArshad()

        class Meta:
            model = Contract
            fields = [
                "id", "title", "dtyp", "initborders", "number", "start_date", "end_date",
                "progress", "is_completed", "department", "mablagh", "moshaver_arshad",
            ]

    class ContractListInputSerializer(serializers.ModelSerializer):
        department = serializers.ChoiceField(
            choices=Contract.DEPARTMENT_CHOICES,
            required=False,
            allow_null=True,
            allow_blank=True,
            error_messages={
                "invalid_choice": f'انتخاب نامعتبر است. گزینه‌های معتبر: {", ".join([f"{choice[0]} ({choice[1]})" for choice in Contract.DEPARTMENT_CHOICES])}'
            },
        )
        moshaver_arshad = serializers.PrimaryKeyRelatedField(
            queryset=Sherkat.objects.all(),
            required=False,
            allow_null=True,
            error_messages={
                "does_not_exist": 'شرکت با شناسه "{pk_value}" یافت نشد.',
                "incorrect_type": "مقدار نامعتبر برای شناسه شرکت: باید عدد باشد.",
            },
        )

        # --- not model fields of Contract ---
        initborder_ids = serializers.PrimaryKeyRelatedField(
            many=True,
            queryset=InitialBorder.objects.all(),
            required=False,
            error_messages={
                "does_not_exist": "محدوده اولیه با شناسه «{pk_value}» یافت نشد.",
                "incorrect_type": "نوع آیدی محدوده اولیه معتبر نمیباشد",
            },
        )

        class ContractListInputSerializerShrhItem(serializers.ModelSerializer):
            shrh_catalog = serializers.PrimaryKeyRelatedField(
                queryset=ShrhCatalog.objects.all(),
                error_messages={
                    "does_not_exist": "بند کاتالوگ با شناسه «{pk_value}» یافت نشد.",
                    "incorrect_type": "نوع آیدی بند کاتالوگ معتبر نمیباشد",
                },
            )

            class Meta:
                model = ShrhContract
                fields = ["shrh_catalog", "scale", "percentage", "worked_percentage"]
                # uniqueness (catalog + scale) is checked in the parent serializer
                validators = []

        shrh_items = ContractListInputSerializerShrhItem(many=True, required=False)

        class Meta:
            model = Contract
            fields = [
                "title", "dtyp", "number", "start_date", "end_date",
                "progress", "is_completed", "department", "mablagh", "moshaver_arshad",
                "initborder_ids", "shrh_items",
            ]

        def validate_moshaver_arshad(self, sherkat):
            if sherkat and not sherkat.mojaz_moshaver_arshad:
                raise serializers.ValidationError("این شرکت مجاز به مشاور ارشد بودن نیست.")
            return sherkat

        def validate(self, attrs):
            ids = attrs.get("initborder_ids", [])
            items = attrs.get("shrh_items", [])
            dtyp = attrs.get("dtyp")

            if len(set(b.pk for b in ids)) != len(ids):
                raise serializers.ValidationError({"initborder_ids": "آیدی محدوده تکراری است"})
            if not ids:
                raise serializers.ValidationError(
                    {"initborder_ids": "حداقل یک محدوده اولیه الزامی است"}
                )

            if items:
                if dtyp is None:
                    raise serializers.ValidationError(
                        {"shrh_items": "برای انتخاب بند، ابتدا باید نوع قرارداد مشخص شود"}
                    )

                errors = {}
                seen = set()
                for index, item in enumerate(items):
                    catalog = item["shrh_catalog"]
                    scale = item.get("scale")
                    if catalog.is_onvan_asli:
                        errors[str(index)] = f"گروه قابل انتخاب نیست؛ فقط بند انتخاب شود. کد گروه: {catalog.code}"
                    elif catalog.contract_domin_id != dtyp.pk:
                        errors[str(index)] = f"نوع قرارداد بند با کد {catalog.code} با نوع قرارداد انتخاب‌شده یکی نیست"
                    elif (catalog.pk, scale) in seen:
                        errors[str(index)] = f"بند با کد {catalog.code} با این مقیاس تکراری است"
                    seen.add((catalog.pk, scale))
                if errors:
                    raise serializers.ValidationError({"shrh_items": errors})
            return attrs

        def create(self, validated_data):
            # these are handled by the view, they are not Contract fields
            for key in ("initborder_ids", "shrh_items"):
                validated_data.pop(key, None)
            return super().create(validated_data)

    def get(self, request: Request) -> Response:
        user: User = request.user
        if user.is_superuser:
            queryset = Contract.objects.all()
        else:
            queryset = user.get_accessible_contracts()

        queryset = (
            self.apply_search(queryset, request)
            .select_related("dtyp", "moshaver_arshad")
            .prefetch_related("initborders")
        )

        paginator = CustomPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.ContractListOutputSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        user: User = request.user

        serializer = self.ContractListInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        existing_borders = data.get("initborder_ids", [])
        shrh_items = data.get("shrh_items", [])

        # one transaction: contract + attaching borders + shrh items + access
        try:
            with transaction.atomic():
                contract = serializer.save()

                ids = [b.pk for b in existing_borders]
                # lock the rows so two requests cannot grab the same border
                locked = list(InitialBorder.objects.select_for_update().filter(pk__in=ids))
                for border in locked:
                    if not user.is_superuser and not user.has_access_to_initialborder(border):
                        raise PermissionDenied("کاربر به این محدوده اولیه دسترسی ندارد")
                    try:
                        # create() (not add()/update()) so that ContractInitialBorder.clean()
                        # runs and rejects borders that still have an active contract
                        ContractInitialBorder.objects.create(contract=contract, initial_border=border)
                    except DjangoValidationError as e:
                        raise ValidationError({"initborder_ids": e.messages})

                # contract_domin of every catalog item was already checked against
                # contract.dtyp in the serializer; package is filled later
                for item in shrh_items:
                    ShrhContract.objects.create(contract=contract, **item)

                user.grant_contract_access(contract=contract)
        except DjangoValidationError as e:
            # model.clean() errors (e.g. start_date > end_date) -> 400 instead of 500,
            # the transaction is already rolled back at this point
            raise ValidationError(e.message_dict if hasattr(e, "error_dict") else e.messages)

        api_activity_logger.info(
            f"ساخت موفق قرارداد {contract.title}",
            extra=get_details_from_request(request),
        )
        return Response(
            self.ContractListOutputSerializer(contract, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class ContractDetailsApiViews(APIView):
    """
    GET: retrieve a contract
    PUT: partial update of a contract
    DELETE: delete a contract (its initial borders are kept, only their links
            to this contract are removed)

    Object-level check: superuser, or a user who has access to this contract.
    """

    class ContractDetailsOutputSerializer(serializers.ModelSerializer):
        class ContractDetailsOutputSerializerDtyp(serializers.ModelSerializer):
            class Meta:
                model = ContractDomin
                fields = ["id", "title", "code"]

        class ContractDetailsOutputSerializerInitborder(serializers.ModelSerializer):
            class ContractDetailsOutputSerializerInitborderDomain(serializers.ModelSerializer):
                class Meta:
                    model = InitialBorderDomin
                    fields = ["id", "title", "code"]

            dtyp = ContractDetailsOutputSerializerInitborderDomain()

            class Meta:
                model = InitialBorder
                fields = ["id", "title", "dtyp"]

        class ContractDetailsOutputSerializerMoshaverArshad(serializers.ModelSerializer):
            class Meta:
                model = Sherkat
                fields = ["id", "name", "typ", "code"]

        dtyp = ContractDetailsOutputSerializerDtyp()
        initborders = ContractDetailsOutputSerializerInitborder(many=True)
        moshaver_arshad = ContractDetailsOutputSerializerMoshaverArshad()

        class Meta:
            model = Contract
            fields = [
                "id", "title", "dtyp", "initborders", "number", "progress", "moshaver_arshad",
                "is_completed", "department", "start_date", "end_date",
                "mablagh", "mablaghe_elhaghye", "tarikh_elhaghye",
                "elhaghye",
            ]

    class ContractDetailsInputSerializer(serializers.ModelSerializer):
        department = serializers.ChoiceField(
            choices=Contract.DEPARTMENT_CHOICES,
            required=False,
            allow_null=True,
            allow_blank=True,
            error_messages={
                "invalid_choice": f'انتخاب نامعتبر است. گزینه‌های معتبر: {", ".join([f"{choice[0]} ({choice[1]})" for choice in Contract.DEPARTMENT_CHOICES])}'
            },
        )
        moshaver_arshad = serializers.PrimaryKeyRelatedField(
            queryset=Sherkat.objects.all(),
            required=False,
            allow_null=True,
            error_messages={
                "does_not_exist": 'شرکت با شناسه "{pk_value}" یافت نشد.',
                "incorrect_type": "مقدار نامعتبر برای شناسه شرکت: باید عدد باشد.",
            },
        )

        class Meta:
            model = Contract
            fields = [
                "title", "dtyp", "number", "start_date", "end_date",
                "progress", "is_completed", "department", "mablagh", "moshaver_arshad",
            ]

        def validate_moshaver_arshad(self, sherkat):
            if sherkat:
                if not sherkat.mojaz_moshaver_arshad:
                    raise serializers.ValidationError("این شرکت مجاز به مشاور ارشد بودن نیست.")
                if self.instance.rsherkatha.filter(sherkat_id=sherkat.pk).exists():
                    raise serializers.ValidationError("این شرکت در همین قرارداد به‌عنوان شرکت اجرایی ثبت شده است.")
            return sherkat

    def _get_contract(self, contractid, queryset=None):
        queryset = queryset if queryset is not None else Contract.objects.all()
        try:
            return queryset.get(pk=contractid), None
        except Contract.DoesNotExist:
            return None, Response({"detail": "قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request: Request, contractid: str) -> Response:
        user: User = request.user
        contract, error = self._get_contract(
            contractid,
            Contract.objects.select_related("dtyp", "moshaver_arshad").prefetch_related("initborders__dtyp"),
        )
        if error:
            return error

        if not user.is_superuser and not user.has_contract_access(contract):
            return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        return Response(self.ContractDetailsOutputSerializer(contract).data)

    def put(self, request: Request, contractid: str) -> Response:
        user: User = request.user
        contract, error = self._get_contract(contractid)
        if error:
            return error

        if not user.is_superuser and not user.has_contract_access(contract):
            return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.ContractDetailsInputSerializer(contract, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            updated_contract = serializer.save()
        except DjangoValidationError as e:
            # model.clean() errors (e.g. start_date > end_date, or re-activating a contract
            # whose borders already have another active contract) -> 400 instead of 500
            raise ValidationError(e.message_dict if hasattr(e, "error_dict") else e.messages)

        return Response(
            self.ContractDetailsOutputSerializer(updated_contract, context={"request": request}).data
        )

    def delete(self, request: Request, contractid: str) -> Response:
        user: User = request.user
        contract, error = self._get_contract(contractid)
        if error:
            return error

        if not user.is_superuser and not user.has_contract_access(contract):
            return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        title = contract.title
        contract.delete()
        delete_logger.warning(f"حذف قرارداد {title}", extra=get_details_from_request(request))
        return Response(status=status.HTTP_204_NO_CONTENT)
# --------------------------------------------------------------------------- #
# ContractElhaghye
# --------------------------------------------------------------------------- #
class ContractElhaghyeListApiViews(APIView):
    """
    GET: elhaghye's of one contract
    POST: add an elhaghye to one contract

    Object-level check through access to the contract.
    """

    class ContractElhaghyeListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractElhaghye
            fields = ["pk", "contract", "title", "mablagh", "tarikh", "description"]

    class ContractElhaghyeListInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractElhaghye
            fields = ["title", "mablagh", "tarikh", "description"]

    def get(self, request: Request, contractid: str) -> Response:
        user: User = request.user
        try:
            contract = Contract.objects.get(pk=contractid)
        except Contract.DoesNotExist:
            return Response({"detail": "قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_contract_access(contract):
            return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        queryset = ContractElhaghye.objects.filter(contract=contract)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.ContractElhaghyeListOutputSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request, contractid: str) -> Response:
        user: User = request.user
        try:
            contract = Contract.objects.get(pk=contractid)
        except Contract.DoesNotExist:
            return Response({"detail": "قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_contract_access(contract):
            return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.ContractElhaghyeListInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        elhaghye = serializer.save(contract=contract)

        return Response(
            self.ContractElhaghyeListOutputSerializer(elhaghye, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

class ContractElhaghyeDetailsApiViews(APIView):
    """
    GET / PUT / DELETE one elhaghye of a contract.

    Object-level check through access to the contract.
    """

    class ContractElhaghyeDetailsOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractElhaghye
            fields = ["pk", "contract", "title", "mablagh", "tarikh", "description"]

    class ContractElhaghyeDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractElhaghye
            fields = ["title", "mablagh", "tarikh", "description"]

    def get(self, request: Request, contractid: str, id: str) -> Response:
        user: User = request.user
        try:
            contract = Contract.objects.get(pk=contractid)
        except Contract.DoesNotExist:
            return Response({"detail": "قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_contract_access(contract):
            return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        try:
            elhaghye = ContractElhaghye.objects.get(pk=id, contract=contract)
        except ContractElhaghye.DoesNotExist:
            return Response({"detail": "الحاقیه‌ای با این آیدی برای این قرارداد وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            self.ContractElhaghyeDetailsOutputSerializer(elhaghye, context={"request": request}).data
        )

    def put(self, request: Request, contractid: str, id: str) -> Response:
        user: User = request.user
        try:
            contract = Contract.objects.get(pk=contractid)
        except Contract.DoesNotExist:
            return Response({"detail": "قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_contract_access(contract):
            return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        try:
            elhaghye = ContractElhaghye.objects.get(pk=id, contract=contract)
        except ContractElhaghye.DoesNotExist:
            return Response({"detail": "الحاقیه‌ای با این آیدی برای این قرارداد وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.ContractElhaghyeDetailsInputSerializer(elhaghye, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_elhaghye = serializer.save()

        return Response(
            self.ContractElhaghyeDetailsOutputSerializer(updated_elhaghye, context={"request": request}).data
        )

    def delete(self, request: Request, contractid: str, id: str) -> Response:
        user: User = request.user
        try:
            contract = Contract.objects.get(pk=contractid)
        except Contract.DoesNotExist:
            return Response({"detail": "قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_contract_access(contract):
            return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        try:
            elhaghye = ContractElhaghye.objects.get(pk=id, contract=contract)
        except ContractElhaghye.DoesNotExist:
            return Response({"detail": "الحاقیه‌ای با این آیدی برای این قرارداد وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        elhaghye.delete()
        delete_logger.warning(
            f"حذف الحاقیه قرارداد {contract.title}", extra=get_details_from_request(request)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
