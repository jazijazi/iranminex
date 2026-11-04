import os
import uuid
import logging
from datetime import datetime

from django.conf import settings
from django.contrib.gis.geos import MultiPolygon
from django.core.validators import FileExtensionValidator
from django.db import transaction

from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from common.mixins import SearchMixin
from common.models import Company, Province
from common.pagination import CustomPagination
from common.services.gis_services import queryset_to_shapefile
from contracts.models.models import (
    Contract,
    ContractBorder,
    ContractDomin,
    ContractElhaghye,
)
from contracts.services.gis import process_contractborder
from initialborders.models.models import InitialBorder, InitialBorderDomin
from logs.utils import get_details_from_request

delete_logger = logging.getLogger("delete_activity_logger")


# --------------------------------------------------------------------------- #
# Contract
# --------------------------------------------------------------------------- #
class ContractListApiViews(SearchMixin, APIView):
    """
    GET: list of contracts (superuser: all, others: only the ones they have access to)

    POST: create a contract together with all of its contract borders at once.
        The request carries a zipped shapefile (rows: <title> <scale> <border>);
        every row becomes one ContractBorder of the new contract.
        Everything is created in one transaction, and the creator gets access
        to the new contract and to all of its contract borders.
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
        initborder = ContractListOutputSerializerInitborder()
        contractborders = serializers.PrimaryKeyRelatedField(
            many=True, read_only=True, source="rcontractborders"
        )

        class Meta:
            model = Contract
            fields = [
                "id", "title", "dtyp", "initborder", "number", "start_date", "end_date",
                "progress", "is_completed", "department", "mablagh", "company",
                "contractborders",
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
        initborder = serializers.PrimaryKeyRelatedField(
            queryset=InitialBorder.objects.all(),
            error_messages={
                "required": "این فیلد اجباری است",
                "does_not_exist": "محدوده اولیه با این آیدی یافت نشد",
                "incorrect_type": "نوع آیدی محدوده اولیه معتبر نمیباشد",
            },
        )
        file = serializers.FileField(
            required=True,
            error_messages={"required": "این فیلد اجباری است"},
            validators=[
                FileExtensionValidator(
                    allowed_extensions=["zip"],
                    message="فایل محدوده حتما باید با فرمت zip باشد",
                )
            ],
        )

        def validate_file(self, value):
            if value.size > 100 * 1024 * 1024:
                raise serializers.ValidationError("File size cannot exceed 100 MB.")
            return value

        class Meta:
            model = Contract
            fields = [
                "title", "dtyp", "initborder", "number", "start_date", "end_date",
                "progress", "is_completed", "department", "mablagh", "company", "file",
            ]

    def get(self, request: Request) -> Response:
        user: User = request.user
        if user.is_superuser:
            queryset = Contract.objects.all()
        else:
            queryset = user.get_accessible_contracts()

        queryset = (
            self.apply_search(queryset, request)
            .select_related("dtyp", "initborder")
            .prefetch_related("company", "rcontractborders")
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

        if not user.is_superuser and not user.has_access_to_initialborder(data["initborder"]):
            return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        # the file is not a Contract field, so take it out before serializer.save()
        zip_file = data.pop("file")

        ok, result_data, message = process_contractborder(zipfile_obj=zip_file)
        if not ok:
            return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)

        if not result_data:
            return Response({"detail": "شیپ فایل هیچ محدوده‌ای ندارد"}, status=status.HTTP_400_BAD_REQUEST)

        if len(result_data) > 50:
            return Response({"detail": "تعداد محدوده‌های قرارداد بیشتر از ۵۰ تا است"}, status=status.HTTP_400_BAD_REQUEST)

        titles = [row["title"] for row in result_data]
        if len(titles) != len(set(titles)):
            return Response({"detail": "عنوان محدوده‌های داخل شیپ فایل تکراری است"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            contract = serializer.save()

            contract_borders = []
            for row in result_data:
                contract_borders.append(
                    ContractBorder.objects.create(
                        contract=contract,
                        title=row["title"],
                        scale=row["scale"],  # may be None
                        border=MultiPolygon(row["border"]),
                    )
                )

            user.grant_contract_access(contract=contract)
            user.grant_bulk_contractborder_access(contractborders=contract_borders)

        return Response(
            self.ContractListOutputSerializer(contract, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class ContractDetailsApiViews(APIView):
    """
    GET: retrieve a contract
    PUT: partial update of a contract (its contract borders are not touched)
    DELETE: delete a contract (its contract borders and elhaghye's are deleted with it)

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
        initborder = ContractDetailsOutputSerializerInitborder()
        company = ContractDetailsOutputSerializerCompany(many=True)
        contractborders = serializers.PrimaryKeyRelatedField(
            many=True, read_only=True, source="rcontractborders"
        )

        class Meta:
            model = Contract
            fields = [
                "id", "title", "dtyp", "initborder", "number", "progress", "company",
                "is_completed", "department", "start_date", "end_date",
                "mablagh", "mablaghe_elhaghye", "tarikh_elhaghye",
                "elhaghye", "contractborders",
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
        initborder = serializers.PrimaryKeyRelatedField(
            queryset=InitialBorder.objects.all(),
            error_messages={
                "does_not_exist": "محدوده اولیه با این آیدی یافت نشد",
                "incorrect_type": "نوع آیدی محدوده اولیه معتبر نمیباشد",
            },
        )

        class Meta:
            model = Contract
            fields = [
                "title", "dtyp", "initborder", "number", "start_date", "end_date",
                "progress", "is_completed", "department", "mablagh", "company",
            ]

    def get(self, request: Request, contractid: str) -> Response:
        user: User = request.user
        try:
            contract = Contract.objects.select_related("dtyp", "initborder__dtyp").get(pk=contractid)
        except Contract.DoesNotExist:
            return Response({"detail": "قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_contract_access(contract):
            return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        return Response(self.ContractDetailsOutputSerializer(contract).data)

    def put(self, request: Request, contractid: str) -> Response:
        user: User = request.user
        try:
            contract = Contract.objects.get(pk=contractid)
        except Contract.DoesNotExist:
            return Response({"detail": "قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_contract_access(contract):
            return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.ContractDetailsInputSerializer(contract, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        new_initborder = serializer.validated_data.get("initborder")
        if new_initborder is not None and not user.is_superuser and not user.has_access_to_initialborder(new_initborder):
            return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        updated_contract = serializer.save()

        return Response(
            self.ContractDetailsOutputSerializer(updated_contract, context={"request": request}).data
        )

    def delete(self, request: Request, contractid: str) -> Response:
        user: User = request.user
        try:
            contract = Contract.objects.get(pk=contractid)
        except Contract.DoesNotExist:
            return Response({"detail": "قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

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
# ContractBorder (its initial border is the initial border of its contract)
# --------------------------------------------------------------------------- #
class ContractBorderListApiView(SearchMixin, APIView):
    """
    GET: list of contract borders
        ?initialborder=<id> only the contract borders of contracts on this initial border
        ?contract=<uuid>    only the contract borders of this contract

    POST: add more contract borders to an existing contract from a zipped shapefile
        (rows: <title> <scale> <border>, one ContractBorder per row)
    """

    search_fields = ["title"]

    class ContractBorderListOutputSerializer(serializers.ModelSerializer):
        class ContractBorderListOutputSerializerContract(serializers.ModelSerializer):
            class Meta:
                model = Contract
                fields = ["id", "title", "number", "start_date", "end_date", "is_completed"]

        class ContractBorderListOutputSerializerInitborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ["id", "title"]

        contract = ContractBorderListOutputSerializerContract()
        initborder = ContractBorderListOutputSerializerInitborder(source="contract.initborder")

        class Meta:
            model = ContractBorder
            fields = ["id", "title", "scale", "center", "bbox", "initborder", "contract"]

    class ContractBorderListInputSerializer(serializers.Serializer):
        file = serializers.FileField(
            required=True,
            error_messages={"required": "این فیلد اجباری است"},
            validators=[
                FileExtensionValidator(
                    allowed_extensions=["zip"],
                    message="فایل محدوده حتما باید با فرمت zip باشد",
                )
            ],
        )
        contract = serializers.PrimaryKeyRelatedField(
            queryset=Contract.objects.all(),
            error_messages={
                "required": "این فیلد اجباری است",
                "does_not_exist": "قراردادی با این آیدی یافت نشد",
                "incorrect_type": "نوع آیدی قرارداد معتبر نمیباشد",
            },
        )

        def validate_file(self, value):
            if value.size > 100 * 1024 * 1024:
                raise serializers.ValidationError("File size cannot exceed 100 MB.")
            return value

    def get(self, request: Request) -> Response:
        user: User = request.user
        if user.is_superuser:
            queryset = ContractBorder.objects.all()
        else:
            queryset = user.get_accessible_contractborders()

        initialborder_param = request.query_params.get("initialborder")
        if initialborder_param:
            if not initialborder_param.isdigit():
                return Response({"initialborder": "شناسه محدوده اولیه معتبر نیست"}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(contract__initborder_id=int(initialborder_param))

        contract_param = request.query_params.get("contract")
        if contract_param:
            try:
                contract_id = uuid.UUID(contract_param)
            except ValueError:
                return Response({"contract": "شناسه قرارداد معتبر نیست"}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(contract_id=contract_id)

        queryset = self.apply_search(queryset, request).select_related("contract__initborder")

        paginator = CustomPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.ContractBorderListOutputSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        user: User = request.user

        serializer = self.ContractBorderListInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        contract = data["contract"]

        if not user.is_superuser and not user.has_contract_access(contract):
            return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        ok, result_data, message = process_contractborder(zipfile_obj=data["file"])
        if not ok:
            return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)

        if len(result_data) > 50:
            return Response({"detail": "تعداد محدوده‌های قرارداد بیشتر از ۵۰ تا است"}, status=status.HTTP_400_BAD_REQUEST)

        titles = [row["title"] for row in result_data]
        if len(titles) != len(set(titles)):
            return Response({"detail": "عنوان محدوده‌های داخل شیپ فایل تکراری است"}, status=status.HTTP_400_BAD_REQUEST)

        # title must be unique inside one contract
        duplicate = ContractBorder.objects.filter(contract=contract, title__in=titles).first()
        if duplicate:
            return Response(
                {"detail": f"محدوده قراردادی با عنوان {duplicate.title} از قبل برای این قرارداد وجود دارد"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            contract_borders = []
            for row in result_data:
                contract_borders.append(
                    ContractBorder.objects.create(
                        contract=contract,
                        title=row["title"],
                        scale=row["scale"],  # may be None
                        border=MultiPolygon(row["border"]),
                    )
                )
            user.grant_bulk_contractborder_access(contractborders=contract_borders)

        return Response(
            self.ContractBorderListOutputSerializer(
                contract_borders, many=True, context={"request": request}
            ).data,
            status=status.HTTP_201_CREATED,
        )


class ContractBorderDetailsApiView(APIView):
    """
    GET: retrieve one contract border
    PUT: replace the title, scale and border of one contract border from a
         zipped shapefile that contains exactly one row
    DELETE: delete one contract border

    Object-level check: superuser, or a user who has access to this contract border.
    """

    class ContractBorderDetailsOutputSerializer(serializers.ModelSerializer):
        class ContractBorderDetailsOutputSerializerContract(serializers.ModelSerializer):
            class ContractBorderDetailsOutputSerializerContractDomain(serializers.ModelSerializer):
                class Meta:
                    model = ContractDomin
                    fields = ["id", "title", "code"]

            dtyp = ContractBorderDetailsOutputSerializerContractDomain()

            class Meta:
                model = Contract
                fields = ["id", "title", "dtyp", "number"]

        class ContractBorderDetailsOutputSerializerInitborder(serializers.ModelSerializer):
            class ContractBorderDetailsOutputSerializerInitborderProvince(serializers.ModelSerializer):
                class Meta:
                    model = Province
                    fields = ["id", "name_fa", "cnter_name_fa", "code"]

            class ContractBorderDetailsOutputSerializerInitborderDomain(serializers.ModelSerializer):
                class Meta:
                    model = InitialBorderDomin
                    fields = ["id", "title", "code"]

            province = ContractBorderDetailsOutputSerializerInitborderProvince(many=True)
            dtyp = ContractBorderDetailsOutputSerializerInitborderDomain()

            class Meta:
                model = InitialBorder
                fields = ["id", "title", "dtyp", "center", "bbox", "parentid", "province"]

        contract = ContractBorderDetailsOutputSerializerContract()
        initborder = ContractBorderDetailsOutputSerializerInitborder(source="contract.initborder")

        class Meta:
            model = ContractBorder
            fields = ["id", "title", "scale", "center", "bbox", "initborder", "contract"]

    class ContractBorderDetailsInputSerializer(serializers.Serializer):
        file = serializers.FileField(
            required=True,
            error_messages={"required": "این فیلد اجباری است"},
            validators=[
                FileExtensionValidator(
                    allowed_extensions=["zip"],
                    message="فایل محدوده حتما باید با فرمت zip باشد",
                )
            ],
        )

        def validate_file(self, value):
            if value.size > 100 * 1024 * 1024:
                raise serializers.ValidationError("File size cannot exceed 100 MB.")
            return value

    def get(self, request: Request, pk: str) -> Response:
        user: User = request.user
        try:
            contractborder = ContractBorder.objects.select_related("contract__dtyp", "contract__initborder__dtyp").get(pk=pk)
        except ContractBorder.DoesNotExist:
            return Response({"detail": "محدوده قراردادی با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_contractborder_access(contractborder):
            return Response({"detail": "کاربر به محدوده قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        return Response(self.ContractBorderDetailsOutputSerializer(contractborder).data)

    def put(self, request: Request, pk: str) -> Response:
        user: User = request.user
        try:
            contractborder = ContractBorder.objects.select_related("contract__dtyp", "contract__initborder__dtyp").get(pk=pk)
        except ContractBorder.DoesNotExist:
            return Response({"detail": "محدوده قراردادی با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_contractborder_access(contractborder):
            return Response({"detail": "کاربر به محدوده قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.ContractBorderDetailsInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ok, result_data, message = process_contractborder(zipfile_obj=serializer.validated_data["file"])
        if not ok:
            return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)

        if len(result_data) != 1:
            return Response(
                {"detail": "برای تغییر محدوده این محدوده قرارداد باید حتما یک محدوده در شیپ فایل وارد شده باشد"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        new_data = result_data[0]

        # another contract border of this contract must not have the same title
        if new_data["title"] != contractborder.title and ContractBorder.objects.filter(
            title=new_data["title"], contract=contractborder.contract
        ).exists():
            return Response(
                {"detail": f"محدوده قراردادی با عنوان {new_data['title']} از قبل برای این قرارداد وجود دارد"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        contractborder.title = new_data["title"]
        contractborder.scale = new_data["scale"]
        contractborder.border = MultiPolygon(new_data["border"])
        contractborder.save()

        return Response(self.ContractBorderDetailsOutputSerializer(contractborder).data)

    def delete(self, request: Request, pk: str) -> Response:
        user: User = request.user
        try:
            contractborder = ContractBorder.objects.get(pk=pk)
        except ContractBorder.DoesNotExist:
            return Response({"detail": "محدوده قراردادی با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_contractborder_access(contractborder):
            return Response({"detail": "کاربر به محدوده قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        title = contractborder.title
        contractborder.delete()
        delete_logger.warning(f"حذف محدوده قرارداد {title}", extra=get_details_from_request(request))
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContractBorderDownloadExportShapeApiViews(APIView):
    def post(self, request: Request, pk: str) -> Response:
        user: User = request.user
        try:
            contractborder = ContractBorder.objects.get(pk=pk)
        except ContractBorder.DoesNotExist:
            return Response({"detail": "محدوده قراردادی با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_contractborder_access(contractborder):
            return Response({"detail": "کاربر به محدوده قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_path = queryset_to_shapefile(
            queryset=ContractBorder.objects.filter(pk=pk),
            geometry_field="border",
            zip_output=True,
            filename=f"contractborder_{pk}_{timestamp}",
        )
        relative_path = os.path.relpath(zip_path, settings.MEDIA_ROOT)
        download_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{relative_path}")

        return Response(
            {"detail": "شیپ فایل با موفقیت ایجاد شد", "download_url": download_url},
            status=status.HTTP_200_OK,
        )


class AllContractBorderDownloadExportShapeApiViews(APIView):
    def post(self, request: Request) -> Response:
        user: User = request.user
        if user.is_superuser:
            queryset = ContractBorder.objects.all()
        else:
            queryset = user.get_accessible_contractborders()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_path = queryset_to_shapefile(
            queryset=queryset,
            geometry_field="border",
            zip_output=True,
            filename=f"allcontractborder_{timestamp}",
        )
        relative_path = os.path.relpath(zip_path, settings.MEDIA_ROOT)
        download_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{relative_path}")

        return Response(
            {"detail": "شیپ فایل با موفقیت ایجاد شد", "download_url": download_url},
            status=status.HTTP_200_OK,
        )


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