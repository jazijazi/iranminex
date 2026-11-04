import os
import logging
from datetime import datetime

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import transaction
from django.db.models import Prefetch

from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from common.mixins import SearchMixin
from common.models import Company, Province
from common.pagination import CustomPagination
from common.services.gis import queryset_to_shapefile
from contracts.models.models import Contract, ContractBorder, ContractDomin
from initialborders.models.attachment import (
    InitialBorderAttachment,
    InitialBorderAttachmentDomain,
)
from initialborders.models.models import InitialBorder, InitialBorderDomin
from initialborders.services.gis import proccess_initialborder_zipfile
from logs.utils import get_details_from_request

delete_logger = logging.getLogger("delete_activity_logger")
api_activity_logger = logging.getLogger("api_activity_logger")


class InitialBorderListViews(SearchMixin, APIView):
    """
    GET: list initial borders (superuser: all, others: only accessible ones)
    POST: create an initial border from a zipped shapefile
    """

    search_fields = ["title", "province__name_fa", "dtyp__title"]

    class InitialBorderListOutputSerializer(serializers.ModelSerializer):
        class InitialBorderListOutputSerializerProvince(serializers.ModelSerializer):
            class Meta:
                model = Province
                fields = ["id", "name_fa", "cnter_name_fa", "code"]

        class InitialBorderListOutputSerializerDomain(serializers.ModelSerializer):
            class Meta:
                model = InitialBorderDomin
                fields = ["id", "title", "code"]

        dtyp = InitialBorderListOutputSerializerDomain()
        province = InitialBorderListOutputSerializerProvince(many=True)

        class Meta:
            model = InitialBorder
            fields = ["id", "title", "dtyp", "province", "center", "bbox", "parentid"]

    class InitialBorderListInputSerializer(serializers.ModelSerializer):
        file = serializers.FileField(
            validators=[
                FileExtensionValidator(
                    allowed_extensions=["zip"],
                    message="فایل محدوده حتما باید با فرمت zip باشد",
                )
            ]
        )

        def validate_file(self, value):
            if value.size > 100 * 1024 * 1024:
                raise serializers.ValidationError("File size cannot exceed 100 MB.")
            return value

        class Meta:
            model = InitialBorder
            fields = ["title", "dtyp", "file", "parentid"]

    def get(self, request: Request) -> Response:
        user: User = request.user
        if user.is_superuser:
            queryset = InitialBorder.objects.all()
        else:
            queryset = user.get_accessible_initialborder()
        queryset = self.apply_search(queryset, request)

        paginator = CustomPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.InitialBorderListOutputSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = self.InitialBorderListInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        ok, border, message = proccess_initialborder_zipfile(data["file"])
        if not ok:
            return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            new_border = InitialBorder.objects.create(
                title=data["title"],
                border=border,
                dtyp=data.get("dtyp"),
                parentid=data.get("parentid"),
            )
            # creator automatically gets access to what they created
            request.user.grant_initialborder_access(initial_border=new_border)

        api_activity_logger.info(
            f"ساخت موفق محدوده اولیه {new_border.title}",
            extra=get_details_from_request(request),
        )
        return Response(self.InitialBorderListOutputSerializer(new_border).data, status=status.HTTP_201_CREATED)


class InitialBorderDetailViews(APIView):
    """GET / PUT / DELETE a single initial border."""

    class InitialBorderDetailOutputSerializer(serializers.ModelSerializer):
        class InitialBorderDetailOutputSerializerProvince(serializers.ModelSerializer):
            class Meta:
                model = Province
                fields = ["id", "name_fa", "cnter_name_fa", "code"]

        class InitialBorderDetailOutputSerializerDomain(serializers.ModelSerializer):
            class Meta:
                model = InitialBorderDomin
                fields = ["id", "title", "code"]

        dtyp = InitialBorderDetailOutputSerializerDomain()
        province = InitialBorderDetailOutputSerializerProvince(many=True)

        class Meta:
            model = InitialBorder
            fields = ["id", "title", "dtyp", "province", "center", "bbox", "parentid"]

    class InitialBorderDetailInputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=250, required=False)
        parentid = serializers.PrimaryKeyRelatedField(
            queryset=InitialBorder.objects.all(), required=False, allow_null=True
        )
        file = serializers.FileField(
            required=False,
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

    def get(self, request: Request, pk: int) -> Response:
        user: User = request.user
        try:
            border = InitialBorder.objects.get(pk=pk)
        except InitialBorder.DoesNotExist:
            return Response({"detail": "محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_access_to_initialborder(border):
            api_activity_logger.warning(
                f"تلاش برای دسترسی غیرمجاز به محدوده اولیه {border.title}",
                extra=get_details_from_request(request),
            )
            return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        return Response(self.InitialBorderDetailOutputSerializer(border).data)

    def put(self, request: Request, pk: int) -> Response:
        user: User = request.user
        try:
            border = InitialBorder.objects.get(pk=pk)
        except InitialBorder.DoesNotExist:
            return Response({"detail": "محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_access_to_initialborder(border):
            api_activity_logger.warning(
                f"تلاش برای ویرایش غیرمجاز محدوده اولیه {border.title}",
                extra=get_details_from_request(request),
            )
            return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.InitialBorderDetailInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if "title" in data:
            border.title = data["title"]

        if "parentid" in data:
            if data["parentid"] is not None and data["parentid"].pk == border.pk:
                return Response({"detail": "محدوده نمی‌تواند والد خودش باشد"}, status=status.HTTP_400_BAD_REQUEST)
            border.parentid = data["parentid"]

        if data.get("file"):
            ok, multipolygon, error = proccess_initialborder_zipfile(data["file"])
            if not ok:
                return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)
            border.border = multipolygon

        border.save()
        api_activity_logger.info(
            f"ویرایش موفق محدوده اولیه {border.title}",
            extra=get_details_from_request(request),
        )
        return Response(self.InitialBorderDetailOutputSerializer(border).data)

    def delete(self, request: Request, pk: int) -> Response:
        user: User = request.user
        try:
            border = InitialBorder.objects.get(pk=pk)
        except InitialBorder.DoesNotExist:
            return Response({"detail": "محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_access_to_initialborder(border):
            api_activity_logger.warning(
                f"تلاش برای حذف غیرمجاز محدوده اولیه {border.title}",
                extra=get_details_from_request(request),
            )
            return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        title = border.title
        border.delete()
        delete_logger.warning(
            f"حذف موفق محدوده اولیه {title}",
            extra=get_details_from_request(request),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class InitialBorderDownloadExportShape(APIView):
    def post(self, request: Request, pk: int) -> Response:
        user: User = request.user
        try:
            border = InitialBorder.objects.get(pk=pk)
        except InitialBorder.DoesNotExist:
            return Response({"detail": "محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_access_to_initialborder(border):
            api_activity_logger.warning(
                f"تلاش برای دسترسی غیرمجاز به محدوده اولیه {border.title}",
                extra=get_details_from_request(request),
            )
            return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_path = queryset_to_shapefile(
            queryset=InitialBorder.objects.filter(pk=pk),
            geometry_field="border",
            zip_output=True,
            filename=f"initialborder_{pk}_{timestamp}",
        )
        relative_path = os.path.relpath(zip_path, settings.MEDIA_ROOT)
        download_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{relative_path}")

        api_activity_logger.info(
            f"شیپ فایل محدوده اولیه {border.title} با موفقیت ایجاد شد",
            extra=get_details_from_request(request),
        )
        return Response(
            {"detail": "شیپ فایل با موفقیت ایجاد شد", "download_url": download_url},
            status=status.HTTP_200_OK,
        )


class AllInitialBorderDownloadExportShape(APIView):
    def post(self, request: Request) -> Response:
        user: User = request.user
        if user.is_superuser:
            queryset = InitialBorder.objects.all()
        else:
            queryset = user.get_accessible_initialborder()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_path = queryset_to_shapefile(
            queryset=queryset,
            geometry_field="border",
            zip_output=True,
            filename=f"allinitialborder_{timestamp}",
        )
        relative_path = os.path.relpath(zip_path, settings.MEDIA_ROOT)
        download_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{relative_path}")

        api_activity_logger.info(
            "شیپ فایل همه محدوده اولیه با موفقیت ایجاد شد",
            extra=get_details_from_request(request),
        )
        return Response(
            {"detail": "شیپ فایل با موفقیت ایجاد شد", "download_url": download_url},
            status=status.HTTP_200_OK,
        )


class InitialBorderDominListView(SearchMixin, APIView):
    permission_classes = [AllowAny]
    search_fields = ["title"]

    class InitialBorderDominListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = InitialBorderDomin
            fields = ["id", "title", "code"]

    def get(self, request: Request) -> Response:
        queryset = self.apply_search(InitialBorderDomin.objects.all(), request)
        return Response(self.InitialBorderDominListOutputSerializer(queryset, many=True).data)

class InitialBorderAttachmentListView(SearchMixin, APIView):
    """
    GET: all attachments of one initial border
    POST: add an attachment to one initial border
    """

    search_fields = ["file"]

    class InitialBorderAttachmentListOutputSerializer(serializers.ModelSerializer):
        class InitialBorderAttachmentListOutputSerializerWriter(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ["username", "first_name_fa", "last_name_fa"]

        class InitialBorderAttachmentListOutputSerializerDtyp(serializers.ModelSerializer):
            class Meta:
                model = InitialBorderAttachmentDomain
                fields = ["id", "code", "name", "category", "dinitialborder"]

        writer = InitialBorderAttachmentListOutputSerializerWriter()
        dtyp_attach = InitialBorderAttachmentListOutputSerializerDtyp()

        class Meta:
            model = InitialBorderAttachment
            fields = ["id", "file", "writer", "upload_date", "writed_date", "dtyp_attach"]

    class InitialBorderAttachmentListInputSerializer(serializers.Serializer):
        file = serializers.FileField()
        writed_date = serializers.DateTimeField(required=False, allow_null=True)
        dtyp_attach = serializers.PrimaryKeyRelatedField(
            queryset=InitialBorderAttachmentDomain.objects.all(),
            error_messages={"does_not_exist": "نوع پیوست یافت نشد"},
        )

    def get(self, request: Request, initialborderpk: int) -> Response:
        user: User = request.user
        try:
            border = InitialBorder.objects.get(pk=initialborderpk)
        except InitialBorder.DoesNotExist:
            return Response({"detail": "محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_access_to_initialborder(border):
            api_activity_logger.warning(
                f"تلاش غیرمجاز برای خواندن پیوست محدوده اولیه {border.title}",
                extra=get_details_from_request(request),
            )
            return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        queryset = InitialBorderAttachment.objects.filter(
            rinitialborder=border
        ).select_related("writer", "dtyp_attach")
        queryset = self.apply_search(queryset, request)

        paginator = CustomPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.InitialBorderAttachmentListOutputSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request, initialborderpk: int) -> Response:
        user: User = request.user
        try:
            border = InitialBorder.objects.get(pk=initialborderpk)
        except InitialBorder.DoesNotExist:
            return Response({"detail": "محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_access_to_initialborder(border):
            api_activity_logger.warning(
                f"تلاش غیرمجاز برای بارگذاری پیوست محدوده اولیه {border.title}",
                extra=get_details_from_request(request),
            )
            return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.InitialBorderAttachmentListInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        attachment = InitialBorderAttachment.objects.create(
            file=data["file"],
            writed_date=data.get("writed_date"),
            dtyp_attach=data["dtyp_attach"],
            writer=user,
            rinitialborder=border,
        )
        api_activity_logger.info(
            f"بارگذاری موفق پیوست محدوده اولیه {border.title}",
            extra=get_details_from_request(request),
        )
        return Response(
            self.InitialBorderAttachmentListOutputSerializer(attachment, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class InitialBorderAttachmentDetailView(APIView):
    """GET / DELETE one attachment (access checked through its initial border)."""

    class InitialBorderAttachmentDetailOutputSerializer(serializers.ModelSerializer):
        class InitialBorderAttachmentDetailOutputSerializerWriter(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ["username", "first_name_fa", "last_name_fa"]

        class InitialBorderAttachmentDetailOutputSerializerDtyp(serializers.ModelSerializer):
            class Meta:
                model = InitialBorderAttachmentDomain
                fields = ["id", "code", "name", "category", "dinitialborder"]

        writer = InitialBorderAttachmentDetailOutputSerializerWriter()
        dtyp_attach = InitialBorderAttachmentDetailOutputSerializerDtyp()

        class Meta:
            model = InitialBorderAttachment
            fields = ["id", "file", "writer", "upload_date", "writed_date", "dtyp_attach"]

    def get(self, request: Request, attachmentpk: int) -> Response:
        user: User = request.user
        try:
            attachment = InitialBorderAttachment.objects.select_related("rinitialborder").get(pk=attachmentpk)
        except InitialBorderAttachment.DoesNotExist:
            return Response({"detail": "پیوست محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_access_to_initialborder(attachment.rinitialborder):
            return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        return Response(self.InitialBorderAttachmentDetailOutputSerializer(attachment, context={"request": request}).data)

    def delete(self, request: Request, attachmentpk: int) -> Response:
        user: User = request.user
        try:
            attachment = InitialBorderAttachment.objects.select_related("rinitialborder").get(pk=attachmentpk)
        except InitialBorderAttachment.DoesNotExist:
            return Response({"detail": "پیوست محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_access_to_initialborder(attachment.rinitialborder):
            return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        path = attachment.file.path
        attachment.delete()
        delete_logger.warning(
            f"حذف پیوست محدوده اولیه {path}",
            extra=get_details_from_request(request),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class InitialBorderAttachmentDomainListApiView(SearchMixin, APIView):
    """GET: list attachment types, POST: create one."""

    search_fields = ["code", "name", "category"]

    class InitialBorderAttachmentDomainListOutputSerializer(serializers.ModelSerializer):
        class InitialBorderAttachmentDomainListOutputSerializerDomain(serializers.ModelSerializer):
            class Meta:
                model = InitialBorderDomin
                fields = ["id", "title", "code"]

        dinitialborder = InitialBorderAttachmentDomainListOutputSerializerDomain()

        class Meta:
            model = InitialBorderAttachmentDomain
            fields = ["id", "code", "name", "category", "dinitialborder"]

    class InitialBorderAttachmentDomainListInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = InitialBorderAttachmentDomain
            fields = ["code", "name", "category", "dinitialborder"]
            extra_kwargs = {"dinitialborder": {"required": True, "allow_null": False}}

    def get(self, request: Request) -> Response:
        queryset = InitialBorderAttachmentDomain.objects.select_related("dinitialborder")
        queryset = self.apply_search(queryset, request)
        return Response(self.InitialBorderAttachmentDomainListOutputSerializer(queryset, many=True).data)

    def post(self, request: Request) -> Response:
        serializer = self.InitialBorderAttachmentDomainListInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        api_activity_logger.info(
            "ساخت موفق نوع پیوست محدوده اولیه",
            extra=get_details_from_request(request),
        )
        return Response(self.InitialBorderAttachmentDomainListOutputSerializer(instance).data, status=status.HTTP_201_CREATED)


class InitialBorderAttachmentDomainDetailsApiView(APIView):
    """GET / PUT / DELETE one attachment type."""

    class InitialBorderAttachmentDomainDetailsOutputSerializer(serializers.ModelSerializer):
        class InitialBorderAttachmentDomainDetailsOutputSerializerDomain(serializers.ModelSerializer):
            class Meta:
                model = InitialBorderDomin
                fields = ["id", "title", "code"]

        dinitialborder = InitialBorderAttachmentDomainDetailsOutputSerializerDomain()

        class Meta:
            model = InitialBorderAttachmentDomain
            fields = ["id", "code", "name", "category", "dinitialborder"]

    class InitialBorderAttachmentDomainDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = InitialBorderAttachmentDomain
            fields = ["code", "name", "category", "dinitialborder"]

    def get(self, request: Request, attachdomainpk: int) -> Response:
        try:
            instance = InitialBorderAttachmentDomain.objects.select_related("dinitialborder").get(pk=attachdomainpk)
        except InitialBorderAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست محدوده اولیه با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.InitialBorderAttachmentDomainDetailsOutputSerializer(instance).data)

    def put(self, request: Request, attachdomainpk: int) -> Response:
        try:
            instance = InitialBorderAttachmentDomain.objects.get(pk=attachdomainpk)
        except InitialBorderAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست محدوده اولیه با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.InitialBorderAttachmentDomainDetailsInputSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(self.InitialBorderAttachmentDomainDetailsOutputSerializer(instance).data)

    def delete(self, request: Request, attachdomainpk: int) -> Response:
        try:
            instance = InitialBorderAttachmentDomain.objects.get(pk=attachdomainpk)
        except InitialBorderAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست محدوده اولیه با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        name = instance.name
        instance.delete()
        delete_logger.warning(
            f"حذف نوع پیوست محدوده اولیه {name}",
            extra=get_details_from_request(request),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class InitialBorderContractsApiView(APIView):
    class InitialBorderContractsOutputSerializer(serializers.ModelSerializer):
        class InitialBorderContractsOutputSerializerDtyp(serializers.ModelSerializer):
            class Meta:
                model = ContractDomin
                fields = ["id", "title", "code"]

        class InitialBorderContractsOutputSerializerCompany(serializers.ModelSerializer):
            class Meta:
                model = Company
                fields = ["id", "name", "typ", "service_typ", "code"]

        dtyp = InitialBorderContractsOutputSerializerDtyp()
        company = InitialBorderContractsOutputSerializerCompany(many=True)
        contractborders = serializers.PrimaryKeyRelatedField(
            many=True, read_only=True, source="rcontractborders"
        )

        class Meta:
            model = Contract
            fields = [
                "id", "title", "dtyp", "number", "progress", "company",
                "is_completed", "department", "mablagh", "mablaghe_elhaghye",
                "tarikh_elhaghye", "start_date", "end_date", "elhaghye",
                "contractborders",
            ]

    def get(self, request: Request, initialborderpk: int) -> Response:
        """Contracts linked to the border; non-superusers see only their own."""
        user: User = request.user
        try:
            border = InitialBorder.objects.get(pk=initialborderpk)
        except InitialBorder.DoesNotExist:
            return Response({"detail": "محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_access_to_initialborder(border):
            return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        contracts = (
            Contract.objects.filter(rcontractborders__initborder=border)
            .select_related("dtyp")
            .prefetch_related(
                "company",
                Prefetch(
                    "rcontractborders",
                    queryset=ContractBorder.objects.filter(initborder=border),
                ),
            )
            .distinct()
        )

        if not user.is_superuser:
            contracts = contracts.filter(
                id__in=user.accessible_contracts.values_list("id", flat=True)
            )

        return Response(self.InitialBorderContractsOutputSerializer(contracts, many=True).data)