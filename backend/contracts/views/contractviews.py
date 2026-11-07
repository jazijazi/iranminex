import os
import uuid
import logging
from datetime import datetime

from django.conf import settings
from django.contrib.gis.geos import MultiPolygon
from django.core.validators import FileExtensionValidator
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from common.mixins import SearchMixin
from common.models.other import Company
from common.pagination import CustomPagination
from common.services.gis import queryset_to_shapefile
from initialborders.services.gis import proccess_initialborder_zipfile
from contracts.models.models import (
    Contract,
    ContractDomin,
    ContractElhaghye,
)
from initialborders.models.models import InitialBorder, InitialBorderDomin
from logs.utils import get_details_from_request

delete_logger = logging.getLogger("delete_activity_logger")
api_activity_logger = logging.getLogger("api_activity_logger")


# --------------------------------------------------------------------------- #
# Contract
# --------------------------------------------------------------------------- #
class ContractListApiViews(SearchMixin, APIView):
    """
    GET: list of contracts (superuser: all, others: only the ones they have access to)

    POST (multipart/form-data): create a contract together with its initial borders.
        A contract can get initial borders in two ways, at the same time:
          - initborder_ids          : ids of already existing initial borders
                                      (must not belong to another contract)
          - new_initborder_files    : zipped shapefiles, one border per file
            new_initborder_titles   : one title per file, same order / same count
        At least one border is required. Everything is created in ONE transaction:
        if any part fails, nothing is saved.
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

        dtyp = ContractListOutputSerializerDtyp()
        initborders = ContractListOutputSerializerInitborder(many=True)

        class Meta:
            model = Contract
            fields = [
                "id", "title", "dtyp", "initborders", "number", "start_date", "end_date",
                "progress", "is_completed", "department", "mablagh", "company",
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
        company = serializers.PrimaryKeyRelatedField(
            many=True,
            queryset=Company.objects.all(),
            error_messages={
                "does_not_exist": 'شرکت با شناسه "{pk_value}" یافت نشد.',
                "incorrect_type": "مقدار نامعتبر برای شناسه شرکت: باید عدد باشد.",
            },
        )

        # --- initial borders (not model fields of Contract) ---
        initborder_ids = serializers.PrimaryKeyRelatedField(
            many=True,
            queryset=InitialBorder.objects.all(),
            required=False,
            error_messages={
                "does_not_exist": "محدوده اولیه با شناسه «{pk_value}» یافت نشد.",
                "incorrect_type": "نوع آیدی محدوده اولیه معتبر نمیباشد",
            },
        )
        new_initborder_files = serializers.ListField(
            child=serializers.FileField(
                validators=[
                    FileExtensionValidator(
                        allowed_extensions=["zip"],
                        message="فایل محدوده حتما باید با فرمت zip باشد",
                    )
                ]
            ),
            required=False,
        )
        new_initborder_titles = serializers.ListField(
            child=serializers.CharField(max_length=250),
            required=False,
        )

        class Meta:
            model = Contract
            fields = [
                "title", "dtyp", "number", "start_date", "end_date",
                "progress", "is_completed", "department", "mablagh", "company",
                "initborder_ids", "new_initborder_files", "new_initborder_titles",
            ]

        def validate_new_initborder_files(self, files):
            for f in files:
                if f.size > 100 * 1024 * 1024:
                    raise serializers.ValidationError(f"File size cannot exceed 100 MB: {f.name}")
            return files

        def validate(self, attrs):
            files = attrs.get("new_initborder_files", [])
            titles = attrs.get("new_initborder_titles", [])
            ids = attrs.get("initborder_ids", [])

            if len(files) != len(titles):
                raise serializers.ValidationError(
                    {"new_initborder_titles": "تعداد عنوان‌ها باید با تعداد فایل‌ها برابر باشد"}
                )
            if len(set(b.pk for b in ids)) != len(ids):
                raise serializers.ValidationError({"initborder_ids": "آیدی محدوده تکراری است"})
            if not files and not ids:
                raise serializers.ValidationError(
                    {"initborder_ids": "حداقل یک محدوده اولیه (موجود یا فایل جدید) الزامی است"}
                )
            return attrs

        def create(self, validated_data):
            # these are handled by the view, they are not Contract fields
            for key in ("initborder_ids", "new_initborder_files", "new_initborder_titles"):
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
            .select_related("dtyp")
            .prefetch_related("company", "initborders")
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
        files = data.get("new_initborder_files", [])
        titles = data.get("new_initborder_titles", [])

        # 1) parse the shapefiles BEFORE opening the transaction (it is slow, and
        #    we do not want to hold DB locks while reading zip files)
        parsed_borders = []
        file_errors = {}
        for index, (upload, title) in enumerate(zip(files, titles)):
            ok, geometry, message = proccess_initialborder_zipfile(upload)
            if not ok:
                file_errors[str(index)] = f"{upload.name}: {message}"
            else:
                parsed_borders.append((title, geometry))
        if file_errors:
            raise ValidationError({"new_initborder_files": file_errors})

        # 2) one transaction: contract + new borders + attaching existing borders + access
        with transaction.atomic():
            contract = serializer.save()

            if existing_borders:
                ids = [b.pk for b in existing_borders]
                # lock the rows so two requests cannot grab the same border
                locked = list(InitialBorder.objects.select_for_update().filter(pk__in=ids))
                for border in locked:
                    if border.contract_id is not None:
                        raise ValidationError(
                            {"initborder_ids": f"محدوده «{border.title}» قبلا به قرارداد دیگری اختصاص داده شده است"}
                        )
                    if not user.is_superuser and not user.has_access_to_initialborder(border):
                        raise PermissionDenied("کاربر به این محدوده اولیه دسترسی ندارد")
                # update() does not touch the geometry, so no ostan recalculation is needed
                InitialBorder.objects.filter(pk__in=ids).update(contract=contract)

            for title, geometry in parsed_borders:
                new_border = InitialBorder.objects.create(
                    title=title,
                    border=geometry,
                    contract=contract,
                )
                user.grant_initialborder_access(initial_border=new_border)

            user.grant_contract_access(contract=contract)

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
    PUT: partial update of a contract (its initial borders are managed through
         the initial border endpoints, using their `contract` field)
    DELETE: delete a contract (its initial borders are kept, they just become unattached)

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

        class ContractDetailsOutputSerializerCompany(serializers.ModelSerializer):
            class Meta:
                model = Company
                fields = ["id", "name", "typ", "service_typ", "code"]

        dtyp = ContractDetailsOutputSerializerDtyp()
        initborders = ContractDetailsOutputSerializerInitborder(many=True)
        company = ContractDetailsOutputSerializerCompany(many=True)

        class Meta:
            model = Contract
            fields = [
                "id", "title", "dtyp", "initborders", "number", "progress", "company",
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

        class Meta:
            model = Contract
            fields = [
                "title", "dtyp", "number", "start_date", "end_date",
                "progress", "is_completed", "department", "mablagh", "company",
            ]

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
            Contract.objects.select_related("dtyp").prefetch_related("company", "initborders__dtyp"),
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
        updated_contract = serializer.save()

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


# --------------------------------------------------------------------------- #
# ContractDomin
# --------------------------------------------------------------------------- #
class ContractDomainsListApiView(APIView):
    """GET: list of all contract domains (they are tied to layer names, so they can't be created here)."""

    permission_classes = [AllowAny]

    class ContractDomainsListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractDomin
            fields = ["id", "title", "code"]

    def get(self, request: Request) -> Response:
        queryset = ContractDomin.objects.all()
        return Response(self.ContractDomainsListOutputSerializer(queryset, many=True).data)