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
    ContractDomin,
    ContractElhaghye,
)
from initialborders.models.models import InitialBorder, InitialBorderDomin
from logs.utils import get_details_from_request

delete_logger = logging.getLogger("delete_activity_logger")


# --------------------------------------------------------------------------- #
# Contract
# --------------------------------------------------------------------------- #
class ContractListApiViews(SearchMixin, APIView):
    """
    GET: list of contracts (superuser: all, others: only the ones they have access to)

    POST: create a contract.
        Everything is created in one transaction, and the creator gets access
        to the new contract.
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

        class Meta:
            model = Contract
            fields = [
                "id", "title", "dtyp", "initborder", "number", "start_date", "end_date",
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
        initborder = serializers.PrimaryKeyRelatedField(
            queryset=InitialBorder.objects.all(),
            error_messages={
                "required": "این فیلد اجباری است",
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

    def get(self, request: Request) -> Response:
        user: User = request.user
        if user.is_superuser:
            queryset = Contract.objects.all()
        else:
            queryset = user.get_accessible_contracts()

        queryset = (
            self.apply_search(queryset, request)
            .select_related("dtyp", "initborder")
            .prefetch_related("company")
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

        with transaction.atomic():
            contract = serializer.save()

            user.grant_contract_access(contract=contract)

        return Response(
            self.ContractListOutputSerializer(contract, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class ContractDetailsApiViews(APIView):
    """
    GET: retrieve a contract
    PUT: partial update of a contract
    DELETE: delete a contract (its elhaghye's are deleted with it)

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

        class Meta:
            model = Contract
            fields = [
                "id", "title", "dtyp", "initborder", "number", "progress", "company",
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