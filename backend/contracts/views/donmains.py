import logging

from django.conf import settings
from logs.utils import get_details_from_request

from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.mixins import SearchMixin
from common.pagination import CustomPagination
from accounts.models import User
from contracts.models.models import (
    Vahed,
    Faz,
    ContractDomin,
    NaghshSherkat,
    ContractAttachmentDomain,
    ShrhAttachmentDomain,
)

delete_logger = logging.getLogger("delete_activity_logger")
api_activity_logger = logging.getLogger("api_activity_logger")



class VahedListApiViews(SearchMixin , APIView):
    """
    GET: elhaghye's of one contract
    POST: add an elhaghye to one contract

    Object-level check through access to the contract.
    """
    search_fields = ["title",]

    class VahedListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Vahed
            fields = ["pk","title"]

    class VahedListInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Vahed
            fields = ["title"]

    def get(self, request: Request, contractid: str) -> Response:
        user: User = request.user
        all_vaheds = Vahed.objects.all()
        all_vaheds = self.apply_search(all_vaheds, request)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(all_vaheds, request)
        serializer = self.VahedListOutputSerializer(page, many=True, context={"request": request})
        api_activity_logger.info(f"خواندن لیست همه واحدها" , extra=get_details_from_request(request))

        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request, contractid: str) -> Response:
        user: User = request.user

        serializer = self.VahedListInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_vahed = serializer.save()
        api_activity_logger.info(f"ساخت واحد جدید با نام {new_vahed.title} " , extra=get_details_from_request(request))
        return Response(
            self.VahedListOutputSerializer(new_vahed, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

class VahedDetailsApiViews(APIView):
    """
    GET / PUT / DELETE one vahed instance.
    """

    class VahedDetailsOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Vahed
            fields = ["pk","title"]

    class VahedDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Vahed
            fields = ["title", "mablagh", "tarikh", "description"]

    def get(self, request: Request, id: int) -> Response:
        user: User = request.user
        try:
            vahed = Vahed.objects.get(pk=id)
        except Vahed.DoesNotExist:
            return Response({"detail": "واحدی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        api_activity_logger.info(f"حواندن اطلاعات واحد با نام {vahed.title} " , extra=get_details_from_request(request))

        return Response(
            self.VahedDetailsOutputSerializer(vahed, context={"request": request}).data
        )

    def put(self, request: Request, id: int) -> Response:
        user: User = request.user

        try:
            vahed = Vahed.objects.get(pk=id,)
        except Vahed.DoesNotExist:
            return Response({"detail": "واحدی با این آیدی برای این قرارداد وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        api_activity_logger.info(f"ویرایش واحد با نام {vahed.title} " , extra=get_details_from_request(request))
        serializer = self.VahedDetailsInputSerializer(vahed, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_vahed = serializer.save()

        return Response(
            self.VahedDetailsOutputSerializer(updated_vahed, context={"request": request}).data
        )

    def delete(self, request: Request, id: int) -> Response:
        user: User = request.user

        try:
            vahed = Vahed.objects.get(pk=id)
        except Vahed.DoesNotExist:
            return Response({"detail": "واحدی با این آیدی برای این قرارداد وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        vahed.delete()
        delete_logger.warning(
            f"حذف واحد  {vahed.title}", extra=get_details_from_request(request)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)



class FazListApiViews(SearchMixin, APIView):
    """
    GET: لیست همه فازها
    POST: ساخت یک فاز جدید
    """
    search_fields = ["title",]

    class FazListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Faz
            fields = ["pk", "title", "order"]

    class FazListInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Faz
            fields = ["title", "order"]

    def get(self, request: Request) -> Response:
        user: User = request.user
        all_fazes = Faz.objects.all()
        all_fazes = self.apply_search(all_fazes, request)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(all_fazes, request)
        serializer = self.FazListOutputSerializer(page, many=True, context={"request": request})
        api_activity_logger.info(f"خواندن لیست همه فازها", extra=get_details_from_request(request))

        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        user: User = request.user

        serializer = self.FazListInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_faz = serializer.save()
        api_activity_logger.info(f"ساخت فاز جدید با نام {new_faz.title} ", extra=get_details_from_request(request))
        return Response(
            self.FazListOutputSerializer(new_faz, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

class FazDetailsApiViews(APIView):
    """
    GET / PUT / DELETE one faz instance.
    """

    class FazDetailsOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Faz
            fields = ["pk", "title", "order"]

    class FazDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Faz
            fields = ["title", "order"]

    def get(self, request: Request, id: int) -> Response:
        user: User = request.user
        try:
            faz = Faz.objects.get(pk=id)
        except Faz.DoesNotExist:
            return Response({"detail": "فازی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        api_activity_logger.info(f"خواندن اطلاعات فاز با نام {faz.title} ", extra=get_details_from_request(request))

        return Response(
            self.FazDetailsOutputSerializer(faz, context={"request": request}).data
        )

    def put(self, request: Request, id: int) -> Response:
        user: User = request.user

        try:
            faz = Faz.objects.get(pk=id)
        except Faz.DoesNotExist:
            return Response({"detail": "فازی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        api_activity_logger.info(f"ویرایش فاز با نام {faz.title} ", extra=get_details_from_request(request))
        serializer = self.FazDetailsInputSerializer(faz, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_faz = serializer.save()

        return Response(
            self.FazDetailsOutputSerializer(updated_faz, context={"request": request}).data
        )

    def delete(self, request: Request, id: int) -> Response:
        user: User = request.user

        try:
            faz = Faz.objects.get(pk=id)
        except Faz.DoesNotExist:
            return Response({"detail": "فازی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        faz.delete()
        delete_logger.warning(
            f"حذف فاز  {faz.title}", extra=get_details_from_request(request)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)



class ContractDominListApiViews(SearchMixin, APIView):
    """
    GET: لیست همه انواع قرارداد
    POST: ساخت یک نوع قرارداد جدید
    """
    search_fields = ["title",]

    class ContractDominListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractDomin
            fields = ["pk", "title", "code"]

    class ContractDominListInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractDomin
            fields = ["title", "code"]

    def get(self, request: Request) -> Response:
        user: User = request.user
        all_contract_domins = ContractDomin.objects.all()
        all_contract_domins = self.apply_search(all_contract_domins, request)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(all_contract_domins, request)
        serializer = self.ContractDominListOutputSerializer(page, many=True, context={"request": request})
        api_activity_logger.info(f"خواندن لیست همه انواع قرارداد", extra=get_details_from_request(request))

        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        user: User = request.user

        serializer = self.ContractDominListInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_contract_domin = serializer.save()
        api_activity_logger.info(f"ساخت نوع قرارداد جدید با نام {new_contract_domin.title} ", extra=get_details_from_request(request))
        return Response(
            self.ContractDominListOutputSerializer(new_contract_domin, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

class ContractDominDetailsApiViews(APIView):
    """
    GET / PUT / DELETE one contract domin instance.
    """

    class ContractDominDetailsOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractDomin
            fields = ["pk", "title", "code"]

    class ContractDominDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractDomin
            fields = ["title", "code"]

    def get(self, request: Request, id: int) -> Response:
        user: User = request.user
        try:
            contract_domin = ContractDomin.objects.get(pk=id)
        except ContractDomin.DoesNotExist:
            return Response({"detail": "نوع قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        api_activity_logger.info(f"خواندن اطلاعات نوع قرارداد با نام {contract_domin.title} ", extra=get_details_from_request(request))

        return Response(
            self.ContractDominDetailsOutputSerializer(contract_domin, context={"request": request}).data
        )

    def put(self, request: Request, id: int) -> Response:
        user: User = request.user

        try:
            contract_domin = ContractDomin.objects.get(pk=id)
        except ContractDomin.DoesNotExist:
            return Response({"detail": "نوع قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        api_activity_logger.info(f"ویرایش نوع قرارداد با نام {contract_domin.title} ", extra=get_details_from_request(request))
        serializer = self.ContractDominDetailsInputSerializer(contract_domin, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_contract_domin = serializer.save()

        return Response(
            self.ContractDominDetailsOutputSerializer(updated_contract_domin, context={"request": request}).data
        )

    def delete(self, request: Request, id: int) -> Response:
        user: User = request.user

        try:
            contract_domin = ContractDomin.objects.get(pk=id)
        except ContractDomin.DoesNotExist:
            return Response({"detail": "نوع قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        contract_domin.delete()
        delete_logger.warning(
            f"حذف نوع قرارداد  {contract_domin.title}", extra=get_details_from_request(request)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)



class NaghshSherkatListApiViews(SearchMixin, APIView):
    """
    GET: لیست همه نقش‌های شرکت
    POST: ساخت یک نقش شرکت جدید
    """
    search_fields = ["title",]

    class NaghshSherkatListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = NaghshSherkat
            fields = ["pk", "title"]

    class NaghshSherkatListInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = NaghshSherkat
            fields = ["title"]

    def get(self, request: Request) -> Response:
        user: User = request.user
        all_naghsh_sherkats = NaghshSherkat.objects.all()
        all_naghsh_sherkats = self.apply_search(all_naghsh_sherkats, request)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(all_naghsh_sherkats, request)
        serializer = self.NaghshSherkatListOutputSerializer(page, many=True, context={"request": request})
        api_activity_logger.info(f"خواندن لیست همه نقش‌های شرکت", extra=get_details_from_request(request))

        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        user: User = request.user

        serializer = self.NaghshSherkatListInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_naghsh_sherkat = serializer.save()
        api_activity_logger.info(f"ساخت نقش شرکت جدید با نام {new_naghsh_sherkat.title} ", extra=get_details_from_request(request))
        return Response(
            self.NaghshSherkatListOutputSerializer(new_naghsh_sherkat, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

class NaghshSherkatDetailsApiViews(APIView):
    """
    GET / PUT / DELETE one naghsh sherkat instance.
    """

    class NaghshSherkatDetailsOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = NaghshSherkat
            fields = ["pk", "title"]

    class NaghshSherkatDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = NaghshSherkat
            fields = ["title"]

    def get(self, request: Request, id: int) -> Response:
        user: User = request.user
        try:
            naghsh_sherkat = NaghshSherkat.objects.get(pk=id)
        except NaghshSherkat.DoesNotExist:
            return Response({"detail": "نقش شرکتی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        api_activity_logger.info(f"خواندن اطلاعات نقش شرکت با نام {naghsh_sherkat.title} ", extra=get_details_from_request(request))

        return Response(
            self.NaghshSherkatDetailsOutputSerializer(naghsh_sherkat, context={"request": request}).data
        )

    def put(self, request: Request, id: int) -> Response:
        user: User = request.user

        try:
            naghsh_sherkat = NaghshSherkat.objects.get(pk=id)
        except NaghshSherkat.DoesNotExist:
            return Response({"detail": "نقش شرکتی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        api_activity_logger.info(f"ویرایش نقش شرکت با نام {naghsh_sherkat.title} ", extra=get_details_from_request(request))
        serializer = self.NaghshSherkatDetailsInputSerializer(naghsh_sherkat, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_naghsh_sherkat = serializer.save()

        return Response(
            self.NaghshSherkatDetailsOutputSerializer(updated_naghsh_sherkat, context={"request": request}).data
        )

    def delete(self, request: Request, id: int) -> Response:
        user: User = request.user

        try:
            naghsh_sherkat = NaghshSherkat.objects.get(pk=id)
        except NaghshSherkat.DoesNotExist:
            return Response({"detail": "نقش شرکتی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        naghsh_sherkat.delete()
        delete_logger.warning(
            f"حذف نقش شرکت  {naghsh_sherkat.title}", extra=get_details_from_request(request)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)



class ContractAttachmentDomainListApiViews(SearchMixin, APIView):
    """
    GET: لیست همه انواع پیوست قرارداد
    POST: ساخت یک نوع پیوست قرارداد جدید
    """
    search_fields = ["name_en", "name_fa", "typ"]

    class ContractAttachmentDomainListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractAttachmentDomain
            fields = ["pk", "code", "name_en", "name_fa", "typ"]

    class ContractAttachmentDomainListInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractAttachmentDomain
            fields = ["code", "name_en", "name_fa", "typ"]

    def get(self, request: Request) -> Response:
        user: User = request.user
        all_attachment_domains = ContractAttachmentDomain.objects.all()
        all_attachment_domains = self.apply_search(all_attachment_domains, request)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(all_attachment_domains, request)
        serializer = self.ContractAttachmentDomainListOutputSerializer(page, many=True, context={"request": request})
        api_activity_logger.info(f"خواندن لیست همه انواع پیوست قرارداد", extra=get_details_from_request(request))

        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        user: User = request.user

        serializer = self.ContractAttachmentDomainListInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_attachment_domain = serializer.save()
        api_activity_logger.info(f"ساخت نوع پیوست قرارداد جدید با نام {new_attachment_domain.name_fa} ", extra=get_details_from_request(request))
        return Response(
            self.ContractAttachmentDomainListOutputSerializer(new_attachment_domain, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

class ContractAttachmentDomainDetailsApiViews(APIView):
    """
    GET / PUT / DELETE one contract attachment domain instance.
    """

    class ContractAttachmentDomainDetailsOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractAttachmentDomain
            fields = ["pk", "code", "name_en", "name_fa", "typ"]

    class ContractAttachmentDomainDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractAttachmentDomain
            fields = ["code", "name_en", "name_fa", "typ"]

    def get(self, request: Request, id: int) -> Response:
        user: User = request.user
        try:
            attachment_domain = ContractAttachmentDomain.objects.get(pk=id)
        except ContractAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        api_activity_logger.info(f"خواندن اطلاعات نوع پیوست قرارداد با نام {attachment_domain.name_fa} ", extra=get_details_from_request(request))

        return Response(
            self.ContractAttachmentDomainDetailsOutputSerializer(attachment_domain, context={"request": request}).data
        )

    def put(self, request: Request, id: int) -> Response:
        user: User = request.user

        try:
            attachment_domain = ContractAttachmentDomain.objects.get(pk=id)
        except ContractAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        api_activity_logger.info(f"ویرایش نوع پیوست قرارداد با نام {attachment_domain.name_fa} ", extra=get_details_from_request(request))
        serializer = self.ContractAttachmentDomainDetailsInputSerializer(attachment_domain, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_attachment_domain = serializer.save()

        return Response(
            self.ContractAttachmentDomainDetailsOutputSerializer(updated_attachment_domain, context={"request": request}).data
        )

    def delete(self, request: Request, id: int) -> Response:
        user: User = request.user

        try:
            attachment_domain = ContractAttachmentDomain.objects.get(pk=id)
        except ContractAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        attachment_domain.delete()
        delete_logger.warning(
            f"حذف نوع پیوست قرارداد  {attachment_domain.name_fa}", extra=get_details_from_request(request)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)



class ShrhAttachmentDomainListApiViews(SearchMixin, APIView):
    """
    GET: لیست همه انواع پیوست بند شرح خدمات
    POST: ساخت یک نوع پیوست بند شرح خدمات جدید
    """
    search_fields = ["name_en", "name_fa", "typ"]

    class ShrhAttachmentDomainListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ShrhAttachmentDomain
            fields = ["pk", "code", "name_en", "name_fa", "typ"]

    class ShrhAttachmentDomainListInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ShrhAttachmentDomain
            fields = ["code", "name_en", "name_fa", "typ"]

    def get(self, request: Request) -> Response:
        user: User = request.user
        all_attachment_domains = ShrhAttachmentDomain.objects.all()
        all_attachment_domains = self.apply_search(all_attachment_domains, request)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(all_attachment_domains, request)
        serializer = self.ShrhAttachmentDomainListOutputSerializer(page, many=True, context={"request": request})
        api_activity_logger.info(f"خواندن لیست همه انواع پیوست بند شرح خدمات", extra=get_details_from_request(request))

        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        user: User = request.user

        serializer = self.ShrhAttachmentDomainListInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_attachment_domain = serializer.save()
        api_activity_logger.info(f"ساخت نوع پیوست بند شرح خدمات جدید با نام {new_attachment_domain.name_fa} ", extra=get_details_from_request(request))
        return Response(
            self.ShrhAttachmentDomainListOutputSerializer(new_attachment_domain, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

class ShrhAttachmentDomainDetailsApiViews(APIView):
    """
    GET / PUT / DELETE one shrh attachment domain instance.
    """

    class ShrhAttachmentDomainDetailsOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ShrhAttachmentDomain
            fields = ["pk", "code", "name_en", "name_fa", "typ"]

    class ShrhAttachmentDomainDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ShrhAttachmentDomain
            fields = ["code", "name_en", "name_fa", "typ"]

    def get(self, request: Request, id: int) -> Response:
        user: User = request.user
        try:
            attachment_domain = ShrhAttachmentDomain.objects.get(pk=id)
        except ShrhAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست بند شرح خدماتی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        api_activity_logger.info(f"خواندن اطلاعات نوع پیوست بند شرح خدمات با نام {attachment_domain.name_fa} ", extra=get_details_from_request(request))

        return Response(
            self.ShrhAttachmentDomainDetailsOutputSerializer(attachment_domain, context={"request": request}).data
        )

    def put(self, request: Request, id: int) -> Response:
        user: User = request.user

        try:
            attachment_domain = ShrhAttachmentDomain.objects.get(pk=id)
        except ShrhAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست بند شرح خدماتی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        api_activity_logger.info(f"ویرایش نوع پیوست بند شرح خدمات با نام {attachment_domain.name_fa} ", extra=get_details_from_request(request))
        serializer = self.ShrhAttachmentDomainDetailsInputSerializer(attachment_domain, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_attachment_domain = serializer.save()

        return Response(
            self.ShrhAttachmentDomainDetailsOutputSerializer(updated_attachment_domain, context={"request": request}).data
        )

    def delete(self, request: Request, id: int) -> Response:
        user: User = request.user

        try:
            attachment_domain = ShrhAttachmentDomain.objects.get(pk=id)
        except ShrhAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست بند شرح خدماتی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)

        attachment_domain.delete()
        delete_logger.warning(
            f"حذف نوع پیوست بند شرح خدمات  {attachment_domain.name_fa}", extra=get_details_from_request(request)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)