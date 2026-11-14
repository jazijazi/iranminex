import logging
from logs.utils import get_details_from_request
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import serializers
from rest_framework.permissions import AllowAny , IsAdminUser
from common.pagination import CustomPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from django.db import transaction
from django.conf import settings
from contracts.filters import (
    ShrhCatalogFilterSet , 
)
from accounts.models import User
from contracts.models.models import (
    Contract,
)
from contracts.models.SharhKhadamats import (
    Faz,
    Vahed,
    ShrhCatalog,
    ShrhContract,
    SherkatContract,
    NaghshSherkat,
    PackageShrh,
)
from common.models.other import Sherkat
from common.mixins import SearchMixin , FilterMixin

from contracts.services.gis import proccess_package_contract_kader__zipfile

delete_logger = logging.getLogger('delete_activity_logger')
api_activity_logger = logging.getLogger("api_activity_logger")

class ShrhCatalogListApiViews(SearchMixin, FilterMixin, APIView):
    """
    GET: لیست کاتالوگ شرح خدمات
    POST: ساخت یک بند / گروه جدید در کاتالوگ شرح خدمات
    """
    search_fields = ["title",]
    filterset_class = ShrhCatalogFilterSet

    class ShrhCatalogListOutputSerializer(serializers.ModelSerializer):
        contract_domin_title = serializers.CharField(source="contract_domin.title", read_only=True)
        faz_title = serializers.CharField(source="faz.title", read_only=True)
        vahed_title = serializers.CharField(source="vahed.title", read_only=True, default=None)

        class Meta:
            model = ShrhCatalog
            fields = [
                "pk", "title", "is_onvan_asli", "order",
                "contract_domin", "contract_domin_title",
                "faz", "faz_title",
                "parent",
                "vahed", "vahed_title",
            ]

    class ShrhCatalogListInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ShrhCatalog
            fields = ["contract_domin", "faz", "parent", "is_onvan_asli", "title", "vahed", "description", "order"]

        def validate(self, attrs):
            """
            همان قوانین ShrhCatalog.clean() در سطح serializer، تا خطا به‌جای 500
            به‌صورت 400 برگردد.
            """
            parent = attrs.get("parent")
            faz = attrs.get("faz")
            is_onvan_asli = attrs.get("is_onvan_asli")
            vahed = attrs.get("vahed")

            errors = {}
            if parent:
                if not parent.is_onvan_asli:
                    errors["parent"] = "عنوان اصلی باید یک گروه باشد."
                elif faz is None or parent.faz_id != faz.pk:
                    errors["faz"] = "فاز بند باید با فاز گروه عنوان اصلی یکی باشد."
            if is_onvan_asli and vahed:
                errors["vahed"] = "گروه واحد ندارد."

            if errors:
                raise serializers.ValidationError(errors)
            return attrs

    def get(self, request: Request) -> Response:
        user: User = request.user
        all_catalogs = ShrhCatalog.objects.select_related("contract_domin", "faz", "vahed")
        all_karbargfive = self.apply_filterset(all_catalogs, request)
        all_catalogs = self.apply_search(all_catalogs, request)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(all_catalogs, request)
        serializer = self.ShrhCatalogListOutputSerializer(page, many=True, context={"request": request})
        api_activity_logger.info(f"خواندن لیست کاتالوگ شرح خدمات", extra=get_details_from_request(request))

        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        user: User = request.user

        serializer = self.ShrhCatalogListInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_catalog = serializer.save()
        api_activity_logger.info(f"ساخت بند جدید کاتالوگ شرح خدمات با نام {new_catalog.title} ", extra=get_details_from_request(request))
        return Response(
            self.ShrhCatalogListOutputSerializer(new_catalog, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

class ShrhCatalogDetailsApiViews(APIView):
    """
    GET / PUT / DELETE one shrh catalog instance.
    """

    class ShrhCatalogDetailsOutputSerializer(serializers.ModelSerializer):
        contract_domin_title = serializers.CharField(source="contract_domin.title", read_only=True)
        faz_title = serializers.CharField(source="faz.title", read_only=True)
        vahed_title = serializers.CharField(source="vahed.title", read_only=True, default=None)

        class Meta:
            model = ShrhCatalog
            fields = [
                "pk","title", "is_onvan_asli", "description", "order",
                "contract_domin", "contract_domin_title",
                "faz", "faz_title",
                "parent",
                "vahed", "vahed_title",
            ]

    class ShrhCatalogDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ShrhCatalog
            fields = ["contract_domin", "faz", "parent", "is_onvan_asli", "title", "vahed", "description", "order"]

        def validate(self, attrs):
            """
            همان قوانین ShrhCatalog.clean() در سطح serializer، تا خطا به‌جای 500
            به‌صورت 400 برگردد. چون ویرایش partial است، فیلدهای ارسال‌نشده
            از خود رکورد (self.instance) خوانده می‌شوند.
            """
            def get(name):
                if name in attrs:
                    return attrs[name]
                return getattr(self.instance, name, None)

            parent = get("parent")
            faz = get("faz")
            is_onvan_asli = get("is_onvan_asli")
            vahed = get("vahed")

            errors = {}
            if parent:
                if parent.pk == self.instance.pk:
                    errors["parent"] = "یک بند نمی‌تواند عنوان اصلی خودش باشد."
                elif not parent.is_onvan_asli:
                    errors["parent"] = "عنوان اصلی باید یک گروه باشد."
                elif faz is None or parent.faz_id != faz.pk:
                    errors["faz"] = "فاز بند باید با فاز گروه عنوان اصلی یکی باشد."
            if is_onvan_asli and vahed:
                errors["vahed"] = "گروه واحد ندارد."

            if errors:
                raise serializers.ValidationError(errors)
            return attrs

    def get(self, request: Request, id: int) -> Response:
        user: User = request.user
        try:
            catalog = ShrhCatalog.objects.select_related("contract_domin", "faz", "vahed").get(pk=id)
        except ShrhCatalog.DoesNotExist:
            return Response({"detail": "بندی با این آیدی در کاتالوگ شرح خدمات وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        api_activity_logger.info(f"خواندن اطلاعات بند کاتالوگ شرح خدمات با نام {catalog.title} ", extra=get_details_from_request(request))

        return Response(
            self.ShrhCatalogDetailsOutputSerializer(catalog, context={"request": request}).data
        )

    def put(self, request: Request, id: int) -> Response:
        user: User = request.user

        try:
            catalog = ShrhCatalog.objects.get(pk=id)
        except ShrhCatalog.DoesNotExist:
            return Response({"detail": "بندی با این آیدی در کاتالوگ شرح خدمات وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        api_activity_logger.info(f"ویرایش بند کاتالوگ شرح خدمات با نام {catalog.title} ", extra=get_details_from_request(request))
        serializer = self.ShrhCatalogDetailsInputSerializer(catalog, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_catalog = serializer.save()

        return Response(
            self.ShrhCatalogDetailsOutputSerializer(updated_catalog, context={"request": request}).data
        )

    def delete(self, request: Request, id: int) -> Response:
        user: User = request.user

        try:
            catalog = ShrhCatalog.objects.get(pk=id)
        except ShrhCatalog.DoesNotExist:
            return Response({"detail": "بندی با این آیدی در کاتالوگ شرح خدمات وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        catalog.delete()
        delete_logger.warning(
            f"حذف بند کاتالوگ شرح خدمات  {catalog.title}", extra=get_details_from_request(request)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)



# ---------------------------------------------------------------------------
# import های لازم (به import قبلی contracts.models.models اضافه شود):
#
# from contracts.models.models import (
#     ...,
#     Contract,
#     ShrhCatalog,
#     ShrhContract,
#     PackageShrh,
# )
# ---------------------------------------------------------------------------


class ShrhContractListApiViews(SearchMixin, APIView):
    """
    GET: بندهای شرح خدمات یک قرارداد
        ?assigned=true|false  -> فقط بندهای اختصاص پکیج‌داده‌شده / آزاد
        ?faz=<id>             -> فقط بندهای یک فاز
    POST: افزودن یک بند از کاتالوگ به قرارداد
        - shrh_catalog      : آیدی بند کاتالوگ (باید «بند» باشد نه گروه، و contract_domin آن
                              با نوع قرارداد (dtyp) یکی باشد)
        - scale             : (اختیاری) مقیاس
        - percentage        : (اختیاری) وزن بند، ۰ تا ۱۰۰
        - worked_percentage : (اختیاری) درصد کار، ۰ تا ۱۰۰
        یک بند با مقیاس‌های مختلف می‌تواند چند بار بیاید؛ بدون مقیاس فقط یک‌بار.
        اختصاص بند به بسته از طریق API بسته‌ها انجام می‌شود، نه اینجا.
    """
    search_fields = ["shrh_catalog__title",]

    class ShrhContractListOutputSerializer(serializers.ModelSerializer):
        class ShrhContractListOutputSerializerFaz(serializers.ModelSerializer):
            class Meta:
                model = Faz
                fields = ["id", "title", "order"]

        class ShrhContractListOutputSerializerVahed(serializers.ModelSerializer):
            class Meta:
                model = Vahed
                fields = ["id", "title"]

        title = serializers.CharField(source="shrh_catalog.title", read_only=True)
        faz = ShrhContractListOutputSerializerFaz(source="shrh_catalog.faz", read_only=True)
        vahed = ShrhContractListOutputSerializerVahed(source="shrh_catalog.vahed", read_only=True)

        class Meta:
            model = ShrhContract
            fields = [
                "pk", "shrh_catalog", "title", "faz", "vahed",
                "scale", "percentage", "worked_percentage", "package",
            ]

    class ShrhContractListInputSerializer(serializers.ModelSerializer):
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
            # uniqueness (contract + catalog + scale) is checked in validate()
            validators = []

        def validate(self, attrs):
            contract = self.context["contract"]
            catalog = attrs["shrh_catalog"]
            scale = attrs.get("scale")

            if catalog.is_onvan_asli:
                raise serializers.ValidationError(
                    {"shrh_catalog": "گروه قابل انتخاب نیست؛ باید یک بند انتخاب شود."}
                )
            if contract.dtyp_id is None or catalog.contract_domin_id != contract.dtyp_id:
                raise serializers.ValidationError(
                    {"shrh_catalog": "نوع قرارداد این بند با نوع قرارداد یکی نیست."}
                )
            if ShrhContract.objects.filter(contract=contract, shrh_catalog=catalog, scale=scale).exists():
                raise serializers.ValidationError(
                    {"shrh_catalog": "این بند با همین مقیاس قبلا به قرارداد اضافه شده است."}
                )
            return attrs

    def get(self, request: Request, contractid: str) -> Response:
        user: User = request.user
        try:
            contract = Contract.objects.get(pk=contractid)
        except Contract.DoesNotExist:
            return Response({"detail": "قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_contract_access(contract):
            return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        queryset = ShrhContract.objects.filter(contract=contract).select_related(
            "shrh_catalog", "shrh_catalog__faz", "shrh_catalog__vahed"
        ).order_by("shrh_catalog__order", "pk")

        assigned = request.query_params.get("assigned")
        if assigned == "true":
            queryset = queryset.filter(package__isnull=False)
        elif assigned == "false":
            queryset = queryset.filter(package__isnull=True)
        faz = request.query_params.get("faz")
        if faz:
            queryset = queryset.filter(shrh_catalog__faz_id=faz)

        queryset = self.apply_search(queryset, request)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.ShrhContractListOutputSerializer(page, many=True, context={"request": request})
        api_activity_logger.info(f"خواندن لیست بندهای قرارداد {contract.title}", extra=get_details_from_request(request))

        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request, contractid: str) -> Response:
        user: User = request.user
        try:
            contract = Contract.objects.get(pk=contractid)
        except Contract.DoesNotExist:
            return Response({"detail": "قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_contract_access(contract):
            return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.ShrhContractListInputSerializer(
            data=request.data, context={"request": request, "contract": contract}
        )
        serializer.is_valid(raise_exception=True)
        new_item = serializer.save(contract=contract)

        api_activity_logger.info(
            f"افزودن بند {new_item.shrh_catalog.title} به قرارداد {contract.title}",
            extra=get_details_from_request(request),
        )
        return Response(
            self.ShrhContractListOutputSerializer(new_item, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class ShrhContractDetailsApiViews(APIView):
    """
    GET: جزئیات یک بند قرارداد (همراه محاسبات وزن، درصد تکمیل و مبلغ)
    PUT (partial): ویرایش مقیاس، وزن و درصد کار — بند کاتالوگ و بسته از اینجا تغییر نمی‌کنند
                   (بسته از طریق API بسته‌ها مدیریت می‌شود)
    DELETE: حذف بند از قرارداد — اگر به بسته‌ای اختصاص داده شده باشد، ابتدا باید از بسته خارج شود

    Object-level check: superuser، یا کاربری که به این قرارداد دسترسی دارد.
    """

    class ShrhContractDetailsOutputSerializer(serializers.ModelSerializer):
        class ShrhContractDetailsOutputSerializerCatalog(serializers.ModelSerializer):
            class Meta:
                model = ShrhCatalog
                fields = ["id", "is_onvan_asli", "order", "title"]

        class ShrhContractDetailsOutputSerializerFaz(serializers.ModelSerializer):
            class Meta:
                model = Faz
                fields = ["id", "title", "order"]

        class ShrhContractDetailsOutputSerializerVahed(serializers.ModelSerializer):
            class Meta:
                model = Vahed
                fields = ["id", "title"]

        class ShrhContractDetailsOutputSerializerPackage(serializers.ModelSerializer):
            class Meta:
                model = PackageShrh
                fields = ["id", "kader_name", "scale"]

        shrh_catalog = ShrhContractDetailsOutputSerializerCatalog()
        faz = ShrhContractDetailsOutputSerializerFaz(source="shrh_catalog.faz")
        vahed = ShrhContractDetailsOutputSerializerVahed(source="shrh_catalog.vahed")
        package = ShrhContractDetailsOutputSerializerPackage()

        class Meta:
            model = ShrhContract
            fields = [
                "pk", "shrh_catalog", "faz", "vahed", "scale",
                "percentage", "worked_percentage", "package",
                "completion_percentage", "remaining_percentage", "total_price", "completed_price",
            ]

    class ShrhContractDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ShrhContract
            fields = ["scale", "percentage", "worked_percentage"]
            # uniqueness (contract + catalog + scale) is checked in validate()
            validators = []

        def validate(self, attrs):
            item = self.instance
            if "scale" in attrs:
                scale = attrs["scale"]
                if ShrhContract.objects.filter(
                    contract_id=item.contract_id, shrh_catalog_id=item.shrh_catalog_id, scale=scale
                ).exclude(pk=item.pk).exists():
                    raise serializers.ValidationError(
                        {"scale": "این بند با همین مقیاس قبلا در قرارداد وجود دارد."}
                    )
                package = item.package
                if package and package.scale is not None and scale is not None and package.scale != scale:
                    raise serializers.ValidationError(
                        {"scale": "مقیاس بند با مقیاس کادر بسته یکی نیست."}
                    )
            return attrs

    def _get_item(self, contractid, sharhcontractid):
        try:
            return ShrhContract.objects.select_related(
                "contract", "package", "shrh_catalog", "shrh_catalog__faz", "shrh_catalog__vahed"
            ).get(pk=sharhcontractid, contract_id=contractid), None
        except ShrhContract.DoesNotExist:
            return None, Response(
                {"detail": "بندی با این آیدی برای این قرارداد وجود ندارد"}, status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request: Request, contractid: str, sharhcontractid: int) -> Response:
        user: User = request.user
        item, error = self._get_item(contractid, sharhcontractid)
        if error:
            return error
        if not user.is_superuser and not user.has_contract_access(item.contract):
            return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        api_activity_logger.info(
            f"خواندن اطلاعات بند {item.shrh_catalog.title} قرارداد {item.contract.title}",
            extra=get_details_from_request(request),
        )
        return Response(
            self.ShrhContractDetailsOutputSerializer(item, context={"request": request}).data
        )

    def put(self, request: Request, contractid: str, sharhcontractid: int) -> Response:
        user: User = request.user
        item, error = self._get_item(contractid, sharhcontractid)
        if error:
            return error
        if not user.is_superuser and not user.has_contract_access(item.contract):
            return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.ShrhContractDetailsInputSerializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_item = serializer.save()

        api_activity_logger.info(
            f"ویرایش بند {updated_item.shrh_catalog.title} قرارداد {updated_item.contract.title}",
            extra=get_details_from_request(request),
        )
        return Response(
            self.ShrhContractDetailsOutputSerializer(updated_item, context={"request": request}).data
        )

    def delete(self, request: Request, contractid: str, sharhcontractid: int) -> Response:
        user: User = request.user
        item, error = self._get_item(contractid, sharhcontractid)
        if error:
            return error
        if not user.is_superuser and not user.has_contract_access(item.contract):
            return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        if item.package_id is not None:
            return Response(
                {"detail": "این بند به یک بسته اختصاص داده شده است؛ ابتدا آن را از بسته خارج کنید"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        label = f"{item.shrh_catalog.title} قرارداد {item.contract.title}"
        item.delete()
        delete_logger.warning(f"حذف بند {label}", extra=get_details_from_request(request))
        return Response(status=status.HTTP_204_NO_CONTENT)


# ================================ PackageShrh ================================

# ---------------------------------------------------------------------------
# import های لازم:
#
# from django.core.exceptions import ValidationError as DjangoValidationError
# from django.core.validators import FileExtensionValidator
# from initialborders.services.gis import proccess_initialborder_zipfile
# from contracts.models.models import (
#     Contract, SherkatContract, NaghshSherkat, PackageShrh, ShrhContract,
# )
#
# (import json دیگر لازم نیست)
# ---------------------------------------------------------------------------


class PackageShrhListApiViews(SearchMixin, APIView):
    """
    GET: بسته‌های کار یک قرارداد (?sherkat_contract=<id> برای فیلتر یک شرکت)
    POST (multipart/form-data): در «یک مرحله» شرکت را با نقشش به قرارداد اضافه می‌کند،
    بسته کار را می‌سازد و بندها را به آن اختصاص می‌دهد — فقط مشاور ارشد همان قرارداد.
        - sherkat          : آیدی شرکت
        - naghsh           : آیدی نقش شرکت در این قرارداد
                             (اگر این شرکت+نقش قبلا در قرارداد ثبت نشده باشد، خودکار ثبت می‌شود)
        - shrh_contract_ids: آیدی بندهای (ShrhContract) این قرارداد که به این بسته می‌روند.
                             هر بند باید آزاد باشد و مقیاسش با مقیاس بسته یکی باشد.
        - kader_file       : فایل zip کادر
        - kader_name       : (اختیاری) نام کادر
        - scale            : (اختیاری) مقیاس کادر
    همه‌چیز در یک transaction انجام می‌شود: اگر هر بخشی خطا بدهد، هیچ‌چیز ذخیره نمی‌شود.
    """
    search_fields = ["kader_name", "sherkat_contract__sherkat__name"]

    class PackageShrhListOutputSerializer(serializers.ModelSerializer):
        class PackageShrhListOutputSerializerSherkatContract(serializers.ModelSerializer):
            class PackageShrhListOutputSerializerSherkat(serializers.ModelSerializer):
                class Meta:
                    model = Sherkat
                    fields = ["id", "name", "code"]

            class PackageShrhListOutputSerializerNaghsh(serializers.ModelSerializer):
                class Meta:
                    model = NaghshSherkat
                    fields = ["id", "title"]

            sherkat = PackageShrhListOutputSerializerSherkat()
            naghsh = PackageShrhListOutputSerializerNaghsh()

            class Meta:
                model = SherkatContract
                fields = ["pk", "sherkat", "naghsh"]

        sherkat_contract = PackageShrhListOutputSerializerSherkatContract()
        items_count = serializers.IntegerField(source="rbandha.count", read_only=True)
        vazn_kol = serializers.FloatField(read_only=True)
        pishraft = serializers.FloatField(read_only=True)

        class Meta:
            model = PackageShrh
            fields = [
                "pk", "sherkat_contract", "kader_name", "scale",
                "items_count", "vazn_kol", "pishraft",
            ]

    class PackageShrhListInputSerializer(serializers.ModelSerializer):
        sherkat = serializers.PrimaryKeyRelatedField(
            queryset=Sherkat.objects.all(),
            error_messages={
                "does_not_exist": 'شرکت با شناسه "{pk_value}" یافت نشد.',
                "incorrect_type": "مقدار نامعتبر برای شناسه شرکت: باید عدد باشد.",
            },
        )
        naghsh = serializers.PrimaryKeyRelatedField(
            queryset=NaghshSherkat.objects.all(),
            error_messages={
                "does_not_exist": 'نقش با شناسه "{pk_value}" یافت نشد.',
                "incorrect_type": "مقدار نامعتبر برای شناسه نقش: باید عدد باشد.",
            },
        )
        kader_file = serializers.FileField(
            validators=[
                FileExtensionValidator(
                    allowed_extensions=["zip"],
                    message="فایل کادر حتما باید با فرمت zip باشد",
                )
            ],
        )
        shrh_contract_ids = serializers.PrimaryKeyRelatedField(
            many=True,
            queryset=ShrhContract.objects.all(),
            error_messages={
                "does_not_exist": "بند قرارداد با شناسه «{pk_value}» یافت نشد.",
                "incorrect_type": "نوع آیدی بند قرارداد معتبر نمیباشد",
            },
        )

        class Meta:
            model = PackageShrh
            fields = ["sherkat", "naghsh", "kader_file", "kader_name", "scale", "shrh_contract_ids"]

        def validate_kader_file(self, f):
            if f.size > 100 * 1024 * 1024:
                raise serializers.ValidationError(f"File size cannot exceed 100 MB: {f.name}")
            return f

        def validate(self, attrs):
            contract = self.context["contract"]
            sherkat = attrs["sherkat"]
            items = attrs["shrh_contract_ids"]
            scale = attrs.get("scale")

            if contract.moshaver_arshad_id == sherkat.pk:
                raise serializers.ValidationError(
                    {"sherkat": "مشاور ارشد قرارداد نمی‌تواند به‌عنوان شرکت اجرایی ثبت شود."}
                )
            if not items:
                raise serializers.ValidationError({"shrh_contract_ids": "حداقل یک بند الزامی است"})
            if len(set(i.pk for i in items)) != len(items):
                raise serializers.ValidationError({"shrh_contract_ids": "آیدی بند تکراری است"})

            errors = {}
            for item in items:
                if item.contract_id != contract.pk:
                    errors[str(item.pk)] = "این بند متعلق به این قرارداد نیست"
                elif item.package_id is not None:
                    errors[str(item.pk)] = "این بند قبلا به یک بسته اختصاص داده شده است"
                elif scale is not None and item.scale is not None and item.scale != scale:
                    errors[str(item.pk)] = "مقیاس بند با مقیاس کادر بسته یکی نیست"
            if errors:
                raise serializers.ValidationError({"shrh_contract_ids": errors})
            return attrs

    def get(self, request: Request, contractid: str) -> Response:
        user: User = request.user
        try:
            contract = Contract.objects.get(pk=contractid)
        except Contract.DoesNotExist:
            return Response({"detail": "قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not user.has_contract_access(contract):
            return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        queryset = PackageShrh.objects.filter(sherkat_contract__contract=contract).select_related(
            "sherkat_contract__sherkat", "sherkat_contract__naghsh"
        ).prefetch_related("rbandha").order_by("-created_at")

        sherkat_contract = request.query_params.get("sherkat_contract")
        if sherkat_contract:
            queryset = queryset.filter(sherkat_contract_id=sherkat_contract)

        queryset = self.apply_search(queryset, request)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.PackageShrhListOutputSerializer(page, many=True, context={"request": request})
        api_activity_logger.info(f"خواندن لیست بسته‌های قرارداد {contract.title}", extra=get_details_from_request(request))

        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request, contractid: str) -> Response:
        user: User = request.user
        try:
            contract = Contract.objects.get(pk=contractid)
        except Contract.DoesNotExist:
            return Response({"detail": "قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser and not (user.sherkat_id and user.sherkat_id == contract.moshaver_arshad_id):
            return Response(
                {"detail": "فقط مشاور ارشد این قرارداد می‌تواند بسته بسازد"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.PackageShrhListInputSerializer(
            data=request.data, context={"request": request, "contract": contract}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # 1) خواندن فایل کادر قبل از باز شدن transaction (کند است)
        #    فعلا فقط خوانده می‌شود و geometry در فیلد kader ذخیره می‌شود (kader در مدل الزامی است)
        ok, geometry, message = proccess_package_contract_kader__zipfile(data["kader_file"])
        if not ok:
            raise ValidationError({"kader_file": f"{data['kader_file'].name}: {message}"})

        item_ids = [i.pk for i in data["shrh_contract_ids"]]

        # 2) یک transaction: ثبت شرکت-نقش + ساخت بسته + اتصال بندها
        try:
            with transaction.atomic():
                # قفل بندها تا دو درخواست همزمان یک بند را نگیرند
                locked = list(ShrhContract.objects.select_for_update().filter(pk__in=item_ids))
                for item in locked:
                    if item.package_id is not None:
                        raise ValidationError(
                            {"shrh_contract_ids": f"بند {item.pk} قبلا به یک بسته اختصاص داده شده است"}
                        )

                # شرکت+نقش اگر در این قرارداد نبود ثبت می‌شود، وگرنه همان قبلی استفاده می‌شود
                sherkat_contract, _ = SherkatContract.objects.get_or_create(
                    contract=contract, sherkat=data["sherkat"], naghsh=data["naghsh"]
                )

                package = PackageShrh.objects.create(
                    sherkat_contract=sherkat_contract,
                    kader=geometry,
                    kader_name=data.get("kader_name", ""),
                    scale=data.get("scale"),
                    assigned_by=user,
                )
                # save() تک‌تک تا full_clean مدل (قرارداد و مقیاس) اجرا شود
                for item in locked:
                    item.package = package
                    item.save()
        except DjangoValidationError as e:
            # خطای full_clean مدل‌ها -> 400 به‌جای 500 (transaction همین‌جا rollback شده است)
            raise ValidationError(e.message_dict if hasattr(e, "error_dict") else e.messages)

        api_activity_logger.info(
            f"ساخت بسته کار برای {package.sherkat_contract} با {len(item_ids)} بند",
            extra=get_details_from_request(request),
        )
        return Response(
            self.PackageShrhListOutputSerializer(package, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class PackageShrhDetailsApiViews(APIView):
    """
    GET: جزئیات بسته (همراه بندها)
    PUT (multipart/form-data, partial): ویرایش بسته — فقط مشاور ارشد
        - kader_name, scale
        - kader_file        : (اختیاری) جایگزینی کادر
        - shrh_contract_ids : (اختیاری) لیست کامل بندهای بسته؛ بندهای جدید اضافه
                              و بندهایی که در لیست نیستند آزاد می‌شوند
    DELETE: حذف بسته (بندها آزاد می‌شوند، حذف نمی‌شوند) — فقط مشاور ارشد
    """

    class PackageShrhDetailsOutputSerializer(serializers.ModelSerializer):
        class PackageShrhDetailsOutputSerializerSherkatContract(serializers.ModelSerializer):
            class PackageShrhDetailsOutputSerializerSherkat(serializers.ModelSerializer):
                class Meta:
                    model = Sherkat
                    fields = ["id", "name", "code"]

            class PackageShrhDetailsOutputSerializerNaghsh(serializers.ModelSerializer):
                class Meta:
                    model = NaghshSherkat
                    fields = ["id", "title"]

            sherkat = PackageShrhDetailsOutputSerializerSherkat()
            naghsh = PackageShrhDetailsOutputSerializerNaghsh()

            class Meta:
                model = SherkatContract
                fields = ["pk", "sherkat", "naghsh"]

        class PackageShrhDetailsOutputSerializerItem(serializers.ModelSerializer):
            code = serializers.IntegerField(source="shrh_catalog.code", read_only=True)
            title = serializers.CharField(source="shrh_catalog.title", read_only=True)

            class Meta:
                model = ShrhContract
                fields = ["pk", "shrh_catalog", "code", "title", "scale", "percentage", "worked_percentage"]

        sherkat_contract = PackageShrhDetailsOutputSerializerSherkatContract()
        items = PackageShrhDetailsOutputSerializerItem(source="rbandha", many=True)
        vazn_kol = serializers.FloatField(read_only=True)
        pishraft = serializers.FloatField(read_only=True)

        class Meta:
            model = PackageShrh
            fields = [
                "pk", "sherkat_contract", "kader_name", "scale",
                "assigned_by", "vazn_kol", "pishraft", "items",
            ]

    class PackageShrhDetailsInputSerializer(serializers.ModelSerializer):
        kader_file = serializers.FileField(
            required=False,
            validators=[
                FileExtensionValidator(
                    allowed_extensions=["zip"],
                    message="فایل کادر حتما باید با فرمت zip باشد",
                )
            ],
        )
        shrh_contract_ids = serializers.PrimaryKeyRelatedField(
            many=True,
            required=False,
            queryset=ShrhContract.objects.all(),
            error_messages={
                "does_not_exist": "بند قرارداد با شناسه «{pk_value}» یافت نشد.",
                "incorrect_type": "نوع آیدی بند قرارداد معتبر نمیباشد",
            },
        )

        class Meta:
            model = PackageShrh
            fields = ["kader_file", "kader_name", "scale", "shrh_contract_ids"]

        def validate_kader_file(self, f):
            if f.size > 100 * 1024 * 1024:
                raise serializers.ValidationError(f"File size cannot exceed 100 MB: {f.name}")
            return f

        def validate(self, attrs):
            package = self.instance
            contract_id = package.sherkat_contract.contract_id
            scale = attrs["scale"] if "scale" in attrs else package.scale
            if "shrh_contract_ids" in attrs:
                items = attrs["shrh_contract_ids"]
                if not items:
                    raise serializers.ValidationError(
                        {"shrh_contract_ids": "بسته باید حداقل یک بند داشته باشد؛ برای حذف کامل، خود بسته را حذف کنید"}
                    )
                if len(set(i.pk for i in items)) != len(items):
                    raise serializers.ValidationError({"shrh_contract_ids": "آیدی بند تکراری است"})
            else:
                items = list(package.rbandha.all())

            errors = {}
            for item in items:
                if item.contract_id != contract_id:
                    errors[str(item.pk)] = "این بند متعلق به این قرارداد نیست"
                elif item.package_id not in (None, package.pk):
                    errors[str(item.pk)] = "این بند به بسته دیگری اختصاص داده شده است"
                elif scale is not None and item.scale is not None and item.scale != scale:
                    errors[str(item.pk)] = "مقیاس بند با مقیاس کادر بسته یکی نیست"
            if errors:
                raise serializers.ValidationError({"shrh_contract_ids": errors})
            return attrs

    def _get_package(self, contractid, id):
        try:
            return PackageShrh.objects.select_related(
                "sherkat_contract__contract", "sherkat_contract__sherkat", "sherkat_contract__naghsh"
            ).prefetch_related("rbandha__shrh_catalog").get(
                pk=id, sherkat_contract__contract_id=contractid
            ), None
        except PackageShrh.DoesNotExist:
            return None, Response(
                {"detail": "بسته‌ای با این آیدی برای این قرارداد وجود ندارد"}, status=status.HTTP_404_NOT_FOUND
            )

    def _can_manage(self, user, contract):
        return user.is_superuser or bool(user.sherkat_id and user.sherkat_id == contract.moshaver_arshad_id)

    def get(self, request: Request, contractid: str, id: int) -> Response:
        user: User = request.user
        package, error = self._get_package(contractid, id)
        if error:
            return error
        contract = package.sherkat_contract.contract
        if not user.is_superuser and not user.has_contract_access(contract):
            return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

        api_activity_logger.info(f"خواندن اطلاعات بسته {package}", extra=get_details_from_request(request))
        return Response(
            self.PackageShrhDetailsOutputSerializer(package, context={"request": request}).data
        )

    def put(self, request: Request, contractid: str, id: int) -> Response:
        user: User = request.user
        package, error = self._get_package(contractid, id)
        if error:
            return error
        if not self._can_manage(user, package.sherkat_contract.contract):
            return Response(
                {"detail": "فقط مشاور ارشد این قرارداد می‌تواند بسته را ویرایش کند"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.PackageShrhDetailsInputSerializer(package, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        geometry = None
        if "kader_file" in data:
            ok, geometry, message = proccess_package_contract_kader__zipfile(data["kader_file"])
            if not ok:
                raise ValidationError({"kader_file": f"{data['kader_file'].name}: {message}"})

        try:
            with transaction.atomic():
                if "kader_name" in data:
                    package.kader_name = data["kader_name"]
                if "scale" in data:
                    package.scale = data["scale"]
                if geometry is not None:
                    package.kader = geometry
                package.save()

                if "shrh_contract_ids" in data:
                    new_ids = set(i.pk for i in data["shrh_contract_ids"])
                    current_ids = set(i.pk for i in package.rbandha.all())

                    # آزاد کردن بندهای حذف‌شده از بسته
                    for item in ShrhContract.objects.select_for_update().filter(pk__in=current_ids - new_ids):
                        item.package = None
                        item.save()
                    # افزودن بندهای جدید (قفل + چک دوباره آزاد بودن)
                    for item in ShrhContract.objects.select_for_update().filter(pk__in=new_ids - current_ids):
                        if item.package_id is not None:
                            raise ValidationError(
                                {"shrh_contract_ids": f"بند {item.pk} قبلا به یک بسته اختصاص داده شده است"}
                            )
                        item.package = package
                        item.save()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict if hasattr(e, "error_dict") else e.messages)

        api_activity_logger.info(f"ویرایش بسته {package}", extra=get_details_from_request(request))
        package, _ = self._get_package(contractid, id)  # تازه‌سازی prefetch بندها
        return Response(
            self.PackageShrhDetailsOutputSerializer(package, context={"request": request}).data
        )

    def delete(self, request: Request, contractid: str, id: int) -> Response:
        user: User = request.user
        package, error = self._get_package(contractid, id)
        if error:
            return error
        if not self._can_manage(user, package.sherkat_contract.contract):
            return Response(
                {"detail": "فقط مشاور ارشد این قرارداد می‌تواند بسته را حذف کند"},
                status=status.HTTP_403_FORBIDDEN,
            )

        label = str(package)
        package.delete()  # on_delete=SET_NULL: بندها آزاد می‌شوند
        delete_logger.warning(f"حذف بسته {label}", extra=get_details_from_request(request))
        return Response(status=status.HTTP_204_NO_CONTENT)
    


# class SharhKhadamatLayerListApiView(SearchMixin, APIView):
#     """
#         Get A Contract uuid from url 
#         GET: List of all sharh_layers associated to this Contract base with Shar_base title Seprated
        
#         POST: Creates one or more sharh_layers instances.
#             (Input can be a single object or a list of objects.)
        
#         ****** This endpoint is exclusively for the Admin Page;
#           it doesn't handle user layers or the layer upload form.
#           (Those URLs are in the layers app, not here.) ******

#     """
#     search_fields = ['shrh_base__title',
#                 'layer_name__lyrgroup_en',
#                 'layer_name__lyrgroup_fa',
#                 'layer_name__layername_en',
#                 'layer_name__layername_fa',]
#     class SharhKhadamatLayerListOutputSerializer(serializers.ModelSerializer):
#         class SharhKhadamatLayerListLayername(serializers.ModelSerializer):
#             class Meta:
#                 model = LayersNames
#                 fields = ['id','dtyp','lyrgroup_en','lyrgroup_fa',
#                           'layername_en','layername_fa','geometrytype']
#         class SharhKhadamatLayerListUser(serializers.ModelSerializer):
#             class Meta:
#                 model = User
#                 fields = ['id','username','first_name_fa','last_name_fa']

#         class SharhkhadamatLayerListShrBase(serializers.ModelSerializer):
#             class Meta:
#                 model = ShrhBase
#                 fields = ["id","title"]

                
#         layer_name = SharhKhadamatLayerListLayername()
#         verified_by = SharhKhadamatLayerListUser()
#         shrh_base = SharhkhadamatLayerListShrBase()
#         last_uploaded_by = SharhKhadamatLayerListUser()

#         class Meta:
#             model = ShrhLayer
#             fields = ['id','shrh_base','layer_name','raster_uuid','scale','is_uploaded','status',
#                 'unit','unit_price',
#                 'last_uploaded_date','last_uploaded_by','upload_count','is_verified','verified_by','verified_at',
#                 'layer_weight','layer_volume',]
            
#     class SharhKhadamatLayerListInputSerializer(serializers.ModelSerializer):

#         class Meta:
#             model = ShrhLayer
#             fields = ['shrh_base','layer_name','scale','unit','unit_price',
#                     'layer_weight','layer_volume',]
            
#     def _build_filters(self, request: Request, contractid: str) -> dict:
#         """Build filter dictionary from URL params and query params"""
#         filters = {
#             'shrh_base__contract_id': contractid
#         }
        
#         # Add sharhbase filter if provided
#         sharhbase_id = request.query_params.get('sharhbase')
#         if sharhbase_id:
#             try:
#                 filters['shrh_base_id'] = int(sharhbase_id)
#             except ValueError:
#                 raise ValidationError({"sharhbase": "شناسه شرح پایه معتبر نیست"})
        
#         return filters
    
#     def get(self , request:Request , contractid:str) -> Response:
#         try:
#             # Validate contract exists
#             contract_instance = Contract.objects.get(pk=contractid)

#             # Dose need check user acceess to this contract ???
            
#             # Build filters from request
#             filters = self._build_filters(request, contractid)
            
#             # Get all ShrhLayer objects with applied filters
#             shrh_layers = ShrhLayer.objects.filter(
#                 **filters
#             ).select_related(
#                 'shrh_base', 
#                 'layer_name',
#                 'verified_by',
#                 'last_uploaded_by',
#                 'verified_by'
#             ).order_by('shrh_base__title', 'layer_name__layername_en') 

#             # Apply user permission filtering
#             if not request.user.is_superuser:
#                 # Filter to only layers the user has access to
#                 shrh_layers = shrh_layers.filter(
#                     accessible_by_users=request.user
#             )

#             paginator = CustomPagination()
#             paginated_queryset = paginator.paginate_queryset(shrh_layers, request)
#             serializer = self.SharhKhadamatLayerListOutputSerializer(paginated_queryset, many=True)

#             return paginator.get_paginated_response(serializer.data)
        
#         except Contract.DoesNotExist:
#             return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             print(e)
#         return Response({"detail": "خطا در خواندن لایه‌های شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#     def post(self, request: Request, contractid: str) -> Response:
#         try:
#             contract_instance = Contract.objects.get(pk=contractid)
#         except Contract.DoesNotExist:
#             return Response(
#                 {"detail": "قراردادی با این آیدی وجود ندارد"}, 
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         except Exception as e:
#             return Response(
#                 {"detail": "خطا در یافتن قرارداد"}, 
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#         # Handle both single object and list of objects
#         data = request.data
#         if not isinstance(data, list):
#             data = [data]
        
#         created_layers = []
#         errors = []

#         for index, layer_data in enumerate(data):
#             # Create input serializer for validation
#             input_serializer = self.SharhKhadamatLayerListInputSerializer(data=layer_data)
        
#             if input_serializer.is_valid():
#                 try:
#                     user: User = request.user
#                     # Validate that shrh_base belongs to the contract
#                     shrh_base = input_serializer.validated_data['shrh_base']
#                     if shrh_base.contract != contract_instance:
#                         errors.append({
#                             'index': index,
#                             'error': 'بند شرح خدمات به این قرارداد تعلق ندارد'
#                         })
#                         continue


#                     # Check for duplicate layer (optional business logic) 
#                     existing_layer = ShrhLayer.objects.filter(
#                         shrh_base=shrh_base,
#                         layer_name=input_serializer.validated_data['layer_name'], 
#                         scale = input_serializer.validated_data['scale']
#                     ).first()
                    
#                     if existing_layer:
#                         errors.append({
#                             'index': index,
#                             'error': 'لایه با این مشخصات قبلاً ایجاد شده است'
#                         })
#                         continue

#                     new_layer = ShrhLayer.objects.create(
#                         shrh_base=shrh_base,
#                         layer_name=input_serializer.validated_data['layer_name'],
#                         scale=input_serializer.validated_data.get('scale'),
#                         layer_weight=input_serializer.validated_data.get('layer_weight', 0),
#                         layer_volume=input_serializer.validated_data.get('layer_volume', 0),
#                     )
#                     created_layers.append(new_layer)
                    
#                 except ValidationError as v_error: #database validation error
#                     # Handle Django ValidationError properly
#                     error_message = str(v_error)
#                     if hasattr(v_error, 'message_dict'):
#                         error_message = v_error.message_dict
#                     elif hasattr(v_error, 'messages'):
#                         error_message = v_error.messages
                        
#                     errors.append({
#                         'index': index,
#                         'error': error_message
#                     })

#                 except Exception as create_error:
#                     errors.append({
#                         'index': index,
#                         'error': f'خطا در ایجاد لایه: {str(create_error)}'
#                     })
#             else:
#                 errors.append({
#                     'index': index,
#                     'error': input_serializer.errors
#                 })

#         # Grant access to all created layers at once (bulk operation)
#         if created_layers:
#             user.grant_bulk_sharhlayer_access(sharhlayers=created_layers)
#         # Build response
#         response_data = {}
#         if created_layers:
#             # Serialize created layers using output serializer
#             output_serializer = self.SharhKhadamatLayerListOutputSerializer(
#                 created_layers, many=True
#             )
#             response_data['created_layers'] = output_serializer.data
#             response_data['created_count'] = len(created_layers)
            
#         if errors:
#             response_data['errors'] = errors
#             response_data['error_count'] = len(errors)
        
#         # Determine response status
#         if created_layers and not errors:
#             # All successful
#             return Response(response_data, status=status.HTTP_201_CREATED)
#         elif created_layers and errors:
#             # Partial success
#             return Response(response_data, status=status.HTTP_207_MULTI_STATUS)
#         else:
#             # All failed
#             return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

# class SharhKhadamatLayerDetailApiView(APIView):
#     """
#         Get A SharhLayer id from url 
#         GET: Retrive An Instance of ShrhLayer Modal
#         DELETE: GET An Instance of ShrhLayer And Delete it
#         PUT: Dont have it yet !
        
#         ****** This endpoint is exclusively for the Admin Page;
#           it doesn't handle user layers or the layer upload form.
#           (Those URLs are in the layers app, not here.) ******

#     """
#     class SharhKhadamatLayerDetailOutputSerializer(serializers.ModelSerializer):
#         class SharhKhadamatLayerDetailLayername(serializers.ModelSerializer):
#             class Meta:
#                 model = LayersNames
#                 fields = ['lyrgroup_en','lyrgroup_fa','dtyp',
#                           'layername_en','layername_fa','geometrytype']
#         class SharhKhadamatLayerDetailUser(serializers.ModelSerializer):
#             class Meta:
#                 model = User
#                 fields = ['id','username','first_name_fa','last_name_fa']


                
#         layer_name = SharhKhadamatLayerDetailLayername()
#         verified_by = SharhKhadamatLayerDetailUser()
#         last_uploaded_by = SharhKhadamatLayerDetailUser()

#         class Meta:
#             model = ShrhLayer
#             fields = ['id','shrh_base','layer_name','raster_uuid','scale','is_uploaded','status',
#                 'unit','unit_price',
#                 'last_uploaded_date','last_uploaded_by','upload_count','is_verified','verified_by','verified_at',
#                 'scale','layer_weight','layer_volume',]
            
#     class SharhKhadamatLayerDetailInputputSerializer(serializers.ModelSerializer):

#         def validate(self, data):
#             return data

#         class Meta:
#             model = ShrhLayer
#             fields = ['scale','layer_weight',
#                     'unit','unit_price',
#                     'layer_volume',] 
            
#     def get(self , request:Request , contractid:str ,shrhid:int) -> Response:
#         try:
#             user:User = request.user 
#             contract_instance = Contract.objects.get(pk=contractid)
#             #TODO make it better (check dhrbase exist and shrhlayer related to shrhbase)
#             shrhlayer_instance = ShrhLayer.objects.get(pk=shrhid) 
#             if not user.is_superuser and not user.has_sharhlayer_access(shrhlayer_instance):
#                 return Response({"detail": "کاربر به این لایه شرح خدمات دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
#             serializer = self.SharhKhadamatLayerDetailOutputSerializer(shrhlayer_instance)
#             return Response(serializer.data , status=status.HTTP_200_OK)
#         except Contract.DoesNotExist:
#             return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
#         except ShrhLayer.DoesNotExist:
#             return Response({"detail":"لایه شرح خدماتی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             print(e)
#             return Response({"detail": "خطا در خواندن لایه شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#     def put(self , request:Request , contractid:str ,shrhid:int) -> Response:
#         try:
#             user:User = request.user 
#             contract_instance = Contract.objects.get(pk=contractid)
#             shrhlayer_instance = ShrhLayer.objects.get(pk=shrhid) 
#             if not user.is_superuser and not user.has_sharhlayer_access(shrhlayer_instance):
#                 return Response({"detail": "کاربر به این لایه شرح خدمات دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
#             input_serializer = self.SharhKhadamatLayerDetailInputputSerializer(
#                 shrhlayer_instance,
#                 data=request.data,
#                 partial=True)
#             if not input_serializer.is_valid():
#                 return Response(input_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#             input_serializer.save()
#             output_serializer = self.SharhKhadamatLayerDetailOutputSerializer(shrhlayer_instance)
#             return Response(output_serializer.data , status=status.HTTP_200_OK)
#         except Contract.DoesNotExist:
#             return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
#         except ShrhLayer.DoesNotExist:
#             return Response({"detail":"لایه شرح خدماتی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             print(e)
#             return Response({"detail": "خطا در خواندن لایه شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
#     def delete(self , request:Request , contractid:str ,shrhid:int) -> Response:
#         try:
#             user:User = request.user 
#             contract_instance = Contract.objects.get(pk=contractid)
#             #TODO make it better (check dhrbase exist and shrhlayer related to shrhbase)
#             shrhlayer_instance = ShrhLayer.objects.get(pk=shrhid) 
#             if not user.is_superuser and not user.has_sharhlayer_access(shrhlayer_instance):
#                 return Response({"detail": "کاربر به این لایه شرح خدمات دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
#             shrhlayer_instance.delete()
#             delete_logger.warning(f"حذف لایه {shrhlayer_instance.id} از لایه های شرح خدمات" , extra=get_details_from_request(request))
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Contract.DoesNotExist:
#             return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
#         except ShrhLayer.DoesNotExist:
#             return Response({"detail":"لایه شرح خدماتی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             print(e)
#             return Response({"detail": "خطا در حذف لایه شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            