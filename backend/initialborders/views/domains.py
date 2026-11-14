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
from common.models.districts import Ostan
from common.pagination import CustomPagination
from common.services.gis import queryset_to_shapefile
from contracts.models.models import Contract, ContractDomin
from initialborders.models.attachment import (
    InitialBorderAttachment,
    InitialBorderAttachmentDomain,
)
from initialborders.models.models import InitialBorderDomin , InitialBorderAttachmentDomain , InitialBorderMadeDomin
from initialborders.services.gis import proccess_initialborder_zipfile
from logs.utils import get_details_from_request

delete_logger = logging.getLogger("delete_activity_logger")
api_activity_logger = logging.getLogger("api_activity_logger")


from rest_framework.permissions import AllowAny, IsAuthenticated


class InitialBorderDominListView(SearchMixin, APIView):
    """
    GET: list of all initial border domin types (public)
    POST: create a new initial border domin type (authenticated)
    """
    search_fields = ["title"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    class InitialBorderDominListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = InitialBorderDomin
            fields = ["id", "title", "code"]

    class InitialBorderDominListInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = InitialBorderDomin
            fields = ["title", "code"]

    def get(self, request: Request) -> Response:
        queryset = self.apply_search(InitialBorderDomin.objects.all(), request)
        return Response(self.InitialBorderDominListOutputSerializer(queryset, many=True).data)

    def post(self, request: Request) -> Response:
        serializer = self.InitialBorderDominListInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_item = serializer.save()
        api_activity_logger.info(
            f"ساخت نوع محدوده اولیه جدید با نام {new_item.title}",
            extra=get_details_from_request(request),
        )
        return Response(
            self.InitialBorderDominListOutputSerializer(new_item, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class InitialBorderDominDetailsView(APIView):
    """
    GET / PUT / DELETE one initial border domin instance.
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    class InitialBorderDominDetailsOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = InitialBorderDomin
            fields = ["id", "title", "code"]

    class InitialBorderDominDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = InitialBorderDomin
            fields = ["title", "code"]

    def get(self, request: Request, id: int) -> Response:
        try:
            item = InitialBorderDomin.objects.get(pk=id)
        except InitialBorderDomin.DoesNotExist:
            return Response(
                {"detail": "نوع محدوده اولیه‌ای با این آیدی وجود ندارد"},
                status=status.HTTP_404_NOT_FOUND,
            )

        api_activity_logger.info(
            f"خواندن اطلاعات نوع محدوده اولیه با نام {item.title}",
            extra=get_details_from_request(request),
        )
        return Response(
            self.InitialBorderDominDetailsOutputSerializer(item, context={"request": request}).data
        )

    def put(self, request: Request, id: int) -> Response:
        try:
            item = InitialBorderDomin.objects.get(pk=id)
        except InitialBorderDomin.DoesNotExist:
            return Response(
                {"detail": "نوع محدوده اولیه‌ای با این آیدی وجود ندارد"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.InitialBorderDominDetailsInputSerializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_item = serializer.save()

        api_activity_logger.info(
            f"ویرایش نوع محدوده اولیه با نام {updated_item.title}",
            extra=get_details_from_request(request),
        )
        return Response(
            self.InitialBorderDominDetailsOutputSerializer(updated_item, context={"request": request}).data
        )

    def delete(self, request: Request, id: int) -> Response:
        try:
            item = InitialBorderDomin.objects.get(pk=id)
        except InitialBorderDomin.DoesNotExist:
            return Response(
                {"detail": "نوع محدوده اولیه‌ای با این آیدی وجود ندارد"},
                status=status.HTTP_404_NOT_FOUND,
            )

        item.delete()
        delete_logger.warning(
            f"حذف نوع محدوده اولیه {item.title}",
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

    def get(self, request: Request, id: int) -> Response:
        try:
            instance = InitialBorderAttachmentDomain.objects.select_related("dinitialborder").get(pk=id)
        except InitialBorderAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست محدوده اولیه با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.InitialBorderAttachmentDomainDetailsOutputSerializer(instance).data)

    def put(self, request: Request, id: int) -> Response:
        try:
            instance = InitialBorderAttachmentDomain.objects.get(pk=id)
        except InitialBorderAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست محدوده اولیه با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.InitialBorderAttachmentDomainDetailsInputSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(self.InitialBorderAttachmentDomainDetailsOutputSerializer(instance).data)

    def delete(self, request: Request, id: int) -> Response:
        try:
            instance = InitialBorderAttachmentDomain.objects.get(pk=id)
        except InitialBorderAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست محدوده اولیه با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        name = instance.name
        instance.delete()
        delete_logger.warning(
            f"حذف نوع پیوست محدوده اولیه {name}",
            extra=get_details_from_request(request),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


  
    
class InitialBorderMadeDominListView(SearchMixin, APIView):
    """
    GET: list of all initial border made domin types (public)
    POST: create a new initial border made domin type (authenticated)
    """
    search_fields = ["title"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    class InitialBorderMadeDominListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = InitialBorderMadeDomin
            fields = ["id", "title"]

    class InitialBorderMadeDominListInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = InitialBorderMadeDomin
            fields = ["title"]

    def get(self, request: Request) -> Response:
        queryset = self.apply_search(InitialBorderMadeDomin.objects.all(), request)
        return Response(self.InitialBorderMadeDominListOutputSerializer(queryset, many=True).data)

    def post(self, request: Request) -> Response:
        serializer = self.InitialBorderMadeDominListInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_item = serializer.save()
        api_activity_logger.info(
            f"ساخت نوع ماده محدوده اولیه جدید با نام {new_item.title}",
            extra=get_details_from_request(request),
        )
        return Response(
            self.InitialBorderMadeDominListOutputSerializer(new_item, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

class InitialBorderMadeDominDetailsView(APIView):
    """
    GET / PUT / DELETE one initial border made domin instance.
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    class InitialBorderMadeDominDetailsOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = InitialBorderMadeDomin
            fields = ["id", "title"]

    class InitialBorderMadeDominDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = InitialBorderMadeDomin
            fields = ["title"]

    def get(self, request: Request, id: int) -> Response:
        try:
            item = InitialBorderMadeDomin.objects.get(pk=id)
        except InitialBorderMadeDomin.DoesNotExist:
            return Response(
                {"detail": "نوع ماده محدوده اولیه‌ای با این آیدی وجود ندارد"},
                status=status.HTTP_404_NOT_FOUND,
            )

        api_activity_logger.info(
            f"خواندن اطلاعات نوع ماده محدوده اولیه با نام {item.title}",
            extra=get_details_from_request(request),
        )
        return Response(
            self.InitialBorderMadeDominDetailsOutputSerializer(item, context={"request": request}).data
        )

    def put(self, request: Request, id: int) -> Response:
        try:
            item = InitialBorderMadeDomin.objects.get(pk=id)
        except InitialBorderMadeDomin.DoesNotExist:
            return Response(
                {"detail": "نوع ماده محدوده اولیه‌ای با این آیدی وجود ندارد"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.InitialBorderMadeDominDetailsInputSerializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_item = serializer.save()

        api_activity_logger.info(
            f"ویرایش نوع ماده محدوده اولیه با نام {updated_item.title}",
            extra=get_details_from_request(request),
        )
        return Response(
            self.InitialBorderMadeDominDetailsOutputSerializer(updated_item, context={"request": request}).data
        )

    def delete(self, request: Request, id: int) -> Response:
        try:
            item = InitialBorderMadeDomin.objects.get(pk=id)
        except InitialBorderMadeDomin.DoesNotExist:
            return Response(
                {"detail": "نوع ماده محدوده اولیه‌ای با این آیدی وجود ندارد"},
                status=status.HTTP_404_NOT_FOUND,
            )

        item.delete()
        delete_logger.warning(
            f"حذف نوع ماده محدوده اولیه {item.title}",
            extra=get_details_from_request(request),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)