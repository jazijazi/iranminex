import logging
from logs.utils import get_details_from_request

from django.core.validators import FileExtensionValidator

from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework import serializers
from rest_framework.permissions import AllowAny

from common.pagination import CustomPagination

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from common.mixins import SearchMixin

from contracts.models.models import (
    ContractBorder,
    Contract,
)
from contracts.models.SharhKhadamats import (
    ShrhBase,
)
from contracts.models.attachment import(
    ContractBorderAttachment,
    ContractBorderAttachmentDomain,

    ContractAttachment,
    ContractAttachmentDomain,

    SharhbaseAttachmentDomain,
    SharhbaseAttachment,
)
from accounts.models import(
    User
)

delete_logger = logging.getLogger('delete_activity_logger')

class ContractBorderAttachmentDomainListApiView(SearchMixin, APIView):
    """
        List Of ContractBorder Attachment Domain`s
    """
    search_fields = ['code','name_en','name_fa','typ']
    class ContractBorderAttachmentDomainListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractBorderAttachmentDomain
            fields = ['id' , 'code', 'name_en', 'name_fa', 'typ']

    class ContractBorderAttachmentDomainListInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractBorderAttachmentDomain
            fields = ['code', 'name_en', 'name_fa', 'typ'] 

    def get(self , request:Request) -> Response:
        try:
            all_contractborderattachmentdomain = ContractBorderAttachmentDomain.objects.all()
            # Add Search query param to it
            all_contractborderattachmentdomain = self.apply_search(all_contractborderattachmentdomain, request)
            serializer = self.ContractBorderAttachmentDomainListOutputSerializer(
                all_contractborderattachmentdomain,
                many=True,
                context={'request': request}
            )
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن انواع پیوست های محدوده قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self , request:Request) -> Response:
        try:
            input_serializer = self.ContractBorderAttachmentDomainListInputSerializer(data=request.data)
            if input_serializer.is_valid():
                shrh_instance = input_serializer.save()
                output_serializer = self.ContractBorderAttachmentDomainListOutputSerializer(shrh_instance)
                return Response(output_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ساخت شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ContractBorderAttachmentDomainDetailsApiView(APIView):
    class ContractBorderAttachmentDomainDetailsOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractBorderAttachmentDomain
            fields = ['id' , 'code', 'name_en', 'name_fa', 'typ']

    class ContractBorderAttachmentDomainDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractBorderAttachmentDomain
            fields = ['code', 'name_en', 'name_fa', 'typ'] 

    def get(self , request:Request , pk:int) -> Response:
        try:
            contractborderattachmentdomainـinstance = ContractBorderAttachmentDomain.objects.get(pk=pk)
            serializer = self.ContractBorderAttachmentDomainDetailsOutputSerializer(contractborderattachmentdomainـinstance)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except ContractBorderAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست محدوده قراردادی با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND) 
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن نوع پیوست محدوده قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

    def put(self , request:Request , pk:int) -> Response:
        try:
            contractborderattachmentdomain_instance = ContractBorderAttachmentDomain.objects.get(pk=pk)
            serializer = self.ContractBorderAttachmentDomainDetailsInputSerializer(
                contractborderattachmentdomain_instance, 
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                # Save the updated instance
                updated_instance = serializer.save()
                output_serializer = self.ContractBorderAttachmentDomainDetailsOutputSerializer(updated_instance)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except ContractBorderAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست محدوده قراردادی با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND) 
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ویرایش نوع پیوست محدوده قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self , request:Request , pk:int) -> Response:
        try:
            contractborderattachmentdomainـinstance = ContractBorderAttachmentDomain.objects.get(pk=pk)
            contractborderattachmentdomainـinstance.delete()
            delete_logger.warning(f"حذف نوع پیوست محدوده قرارداد {contractborderattachmentdomainـinstance.name_fa}" , extra=get_details_from_request(request))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ContractBorderAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست محدوده قراردادی با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND) 
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در حذف نوع پیوست محدوده قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ContractBorderAttachmentListApiView(SearchMixin, APIView):
    """
        GET: return all attachment of a contractborder
        POST: create new attachment of a contractborder

        check object-level
        if user is superuser has access 
        else return only thoes check user has access to it via
        shrhlayer -> contractborder
    """
    search_fields = ['file',]

    class ContractBorderAttachmentListOutputSerializer(serializers.ModelSerializer):
        class ContractBorderAttachmentListOutputSerializerUser(serializers.ModelSerializer): 
            class Meta:
                model = User
                fields = ['username' , 'first_name_fa' , 'last_name_fa']
        class ContractBorderAttachmentListOutputSerializerDtyp(serializers.ModelSerializer): 
            class Meta:
                model = ContractBorderAttachmentDomain
                fields = ['id' , 'code', 'name_en', 'name_fa', 'typ']

        writer = ContractBorderAttachmentListOutputSerializerUser()
        dtyp = ContractBorderAttachmentListOutputSerializerDtyp()

        class Meta:
            model = ContractBorderAttachment
            fields = ['id','upload_date','writer','contractborder','dtyp','file',]

    class ContractBorderAttachmentListInputSerializer(serializers.Serializer):
        file = serializers.FileField(required=True,allow_null=False)
        dtyp_attach = serializers.IntegerField(required=True,allow_null=False)

        def validate_dtyp_attach(self, value):
            try:
                dtyp_attach_instance = ContractBorderAttachmentDomain.objects.get(pk=value)
                return value
            except ContractBorderAttachmentDomain.DoesNotExist:
                raise serializers.ValidationError("نوع پیوست یافت نشد")


    def get(self , request:Request , contractborderid:str)-> Response :
        try:
            user : User = request.user
            contractborder_instance = ContractBorder.objects.get(pk=contractborderid)
            if not user.is_superuser and not user.has_contractborder_access(contractborder_instance):
                return Response({"detail": "کاربر به محدوده قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            all_contractborderattachments = ContractBorderAttachment.objects.filter(contractborder=contractborder_instance)
            # Add Search query param to it
            all_contractborderattachments = self.apply_search(all_contractborderattachments, request)
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(all_contractborderattachments, request)
            serializer = self.ContractBorderAttachmentListOutputSerializer(paginated_queryset,many=True,context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        
        except ContractBorder.DoesNotExist:
            return Response({"detail": "محدوده قراردادی با این آیدی یافت نشد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن پیوست های این محدوده قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self , request:Request , contractborderid:str)-> Response :
        try:
            user : User = request.user
            contractborder_instance = ContractBorder.objects.get(pk=contractborderid)
            if not user.is_superuser and not user.has_contractborder_access(contractborder_instance):
                return Response({"detail": "کاربر به محدوده قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            serializer = self.ContractBorderAttachmentListInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data

            dtyp_attach_instance = ContractBorderAttachmentDomain.objects.get(pk=validated_data['dtyp_attach'])

            contractborderattachment_instance = ContractBorderAttachment.objects.create(
                writer = request.user,
                contractborder = contractborder_instance,
                dtyp = dtyp_attach_instance,
                file = validated_data['file'],
            )

            output_serializer = self.ContractBorderAttachmentListOutputSerializer(contractborderattachment_instance,many=False,context={'request': request})
            return Response(output_serializer.data , status=status.HTTP_201_CREATED)
            
        except ContractBorderAttachmentDomain.DoesNotExist:
                raise serializers.ValidationError("نوع پیوست یافت نشد")
        except ContractBorder.DoesNotExist:
            return Response({"detail": "محدوده قراردادی با این آیدی یافت نشد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ساخت پیوست برای این محدوده قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ContractBorderAttachmentDetailsApiView(APIView):
    """
        GET: return an attachment of a contractborder
        DELETE: delete an attachment of a contractborder

        check object-level
        if user is superuser has access 
        else return only thoes check user has access to it via
        shrhlayer -> contractborder
    """
    class ContractBorderAttachmentDetailsOutputSerializer(serializers.ModelSerializer):
        class ContractBorderAttachmentDetailsOutputSerializerUser(serializers.ModelSerializer): 
            class Meta:
                model = User
                fields = ['username' , 'first_name_fa' , 'last_name_fa']
        class ContractBorderAttachmentDetailsOutputSerializerDtyp(serializers.ModelSerializer): 
            class Meta:
                model = ContractBorderAttachmentDomain
                fields = ['id' , 'code', 'name_en', 'name_fa', 'typ']

        writer = ContractBorderAttachmentDetailsOutputSerializerUser()
        dtyp = ContractBorderAttachmentDetailsOutputSerializerDtyp()

        class Meta:
            model = ContractBorderAttachment
            fields = ['id','upload_date','writer','contractborder','dtyp','file',]

    def get(self , request:Request , contractborderattachmentid:int)-> Response :
        try:
            user : User = request.user
            contractborderattachment_instance = ContractBorderAttachment.objects.get(pk=contractborderattachmentid)
            if not user.is_superuser and not user.has_contractborder_access(contractborderattachment_instance.contractborder):
                return Response({"detail": "کاربر به محدوده قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            serializer = self.ContractBorderAttachmentDetailsOutputSerializer(contractborderattachment_instance,many=False,context={'request': request})
            return Response(serializer.data , status=status.HTTP_200_OK)
        except ContractBorderAttachment.DoesNotExist:
            return Response({"detail": "پیوست محدوده قراردادی با این آیدی یافت نشد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن پیوست محدوده قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # def put ?????

    def delete(self , request:Request , contractborderattachmentid:int)-> Response :
        try:
            user : User = request.user
            contractborderattachment_instance = ContractBorderAttachment.objects.get(pk=contractborderattachmentid)
            if not user.is_superuser and not user.has_contractborder_access(contractborderattachment_instance.contractborder):
                return Response({"detail": "کاربر به محدوده قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            contractborderattachment_instance.delete()
            delete_logger.warning(f"حذف پیوست محدوده قرارداد {contractborderattachment_instance.file.path}" , extra=get_details_from_request(request))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ContractBorderAttachment.DoesNotExist:
            return Response({"detail": "پیوست محدوده قراردادی با این آیدی یافت نشد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در حذف پیوست محدوده قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

### Contract Attach
class ContractAttachmentDomainListApiView(SearchMixin, APIView):
    """
        List Of Contract Attachment Domain`s
    """
    search_fields = ['code','name_en','name_fa','typ']
    class ContractAttachmentDomainListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractAttachmentDomain
            fields = ['id' , 'code', 'name_en', 'name_fa', 'typ']

    class ContractAttachmentDomainListInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractAttachmentDomain
            fields = ['code', 'name_en', 'name_fa', 'typ'] 

    def get(self , request:Request) -> Response:
        try:
            all_ContractAttachmentdomain = ContractAttachmentDomain.objects.all()
            # Add Search query param to it
            all_ContractAttachmentdomain = self.apply_search(all_ContractAttachmentdomain, request)
            serializer = self.ContractAttachmentDomainListOutputSerializer(
                all_ContractAttachmentdomain,
                many=True,
                context={'request': request}
            )
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن انواع پیوست های قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self , request:Request) -> Response:
        try:
            input_serializer = self.ContractAttachmentDomainListInputSerializer(data=request.data)
            if input_serializer.is_valid():
                shrh_instance = input_serializer.save()
                output_serializer = self.ContractAttachmentDomainListOutputSerializer(shrh_instance)
                return Response(output_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ساخت نوع پیوست قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ContractAttachmentDomainDetailsApiView(APIView):
    class ContractAttachmentDomainDetailsOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractAttachmentDomain
            fields = ['id' , 'code', 'name_en', 'name_fa', 'typ']

    class ContractAttachmentDomainDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractAttachmentDomain
            fields = ['code', 'name_en', 'name_fa', 'typ'] 

    def get(self , request:Request , pk:int) -> Response:
        try:
            ContractAttachmentdomainـinstance = ContractAttachmentDomain.objects.get(pk=pk)
            serializer = self.ContractAttachmentDomainDetailsOutputSerializer(ContractAttachmentdomainـinstance)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except ContractAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست قراردادی با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND) 
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن نوع پیوست قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

    def put(self , request:Request , pk:int) -> Response:
        try:
            ContractAttachmentdomain_instance = ContractAttachmentDomain.objects.get(pk=pk)
            serializer = self.ContractAttachmentDomainDetailsInputSerializer(
                ContractAttachmentdomain_instance, 
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                # Save the updated instance
                updated_instance = serializer.save()
                output_serializer = self.ContractAttachmentDomainDetailsOutputSerializer(updated_instance)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except ContractAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست قراردادی با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND) 
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ویرایش نوع پیوست قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self , request:Request , pk:int) -> Response:
        try:
            ContractAttachmentdomainـinstance = ContractAttachmentDomain.objects.get(pk=pk)
            ContractAttachmentdomainـinstance.delete()
            delete_logger.warning(f"حذف نوع پیوست محدوده قرارداد {ContractAttachmentdomainـinstance.name_fa}" , extra=get_details_from_request(request))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ContractAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست قراردادی با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND) 
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در حذف نوع پیوست قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ContractAttachmentListApiView(SearchMixin, APIView):
    """
        GET: return all attachment of a Contract
        POST: create new attachment of a Contract

        check object-level
        if user is superuser has access 
        else return only thoes check user has access to it via Contract
    """
    search_fields = ['file',]

    class ContractAttachmentListOutputSerializer(serializers.ModelSerializer):
        class ContractAttachmentListOutputSerializerUser(serializers.ModelSerializer): 
            class Meta:
                model = User
                fields = ['username' , 'first_name_fa' , 'last_name_fa']
        class ContractAttachmentListOutputSerializerDtyp(serializers.ModelSerializer): 
            class Meta:
                model = ContractAttachmentDomain
                fields = ['id' , 'code', 'name_en', 'name_fa', 'typ']

        writer = ContractAttachmentListOutputSerializerUser()
        dtyp = ContractAttachmentListOutputSerializerDtyp()

        class Meta:
            model = ContractAttachment
            fields = ['id','upload_date','writer','contract','dtyp','file',]

    class ContractAttachmentListInputSerializer(serializers.Serializer):
        file = serializers.FileField(required=True,allow_null=False)
        dtyp_attach = serializers.IntegerField(required=True,allow_null=False)

        def validate_dtyp_attach(self, value):
            try:
                dtyp_attach_instance = ContractAttachmentDomain.objects.get(pk=value)
                return value
            except ContractAttachmentDomain.DoesNotExist:
                raise serializers.ValidationError("نوع پیوست یافت نشد")


    def get(self , request:Request , contractid:str)-> Response :
        try:
            user : User = request.user
            Contract_instance = Contract.objects.get(pk=contractid)
            if not user.is_superuser and not user.has_contract_access(Contract_instance):
                return Response({"detail": "کاربر به  قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            all_ContractAttachments = ContractAttachment.objects.filter(contract=Contract_instance)
            # Add Search query param to it
            all_ContractAttachments = self.apply_search(all_ContractAttachments, request)
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(all_ContractAttachments, request)
            serializer = self.ContractAttachmentListOutputSerializer(paginated_queryset,many=True,context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        
        except Contract.DoesNotExist:
            return Response({"detail": " قراردادی با این آیدی یافت نشد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن پیوست های این قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self , request:Request , contractid:str)-> Response :
        try:
            user : User = request.user
            Contract_instance = Contract.objects.get(pk=contractid)
            if not user.is_superuser and not user.has_contract_access(Contract_instance):
                return Response({"detail": "کاربر به قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            serializer = self.ContractAttachmentListInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data

            dtyp_attach_instance = ContractAttachmentDomain.objects.get(pk=validated_data['dtyp_attach'])

            ContractAttachment_instance = ContractAttachment.objects.create(
                writer = request.user,
                contract = Contract_instance,
                dtyp = dtyp_attach_instance,
                file = validated_data['file'],
            )

            output_serializer = self.ContractAttachmentListOutputSerializer(ContractAttachment_instance,many=False,context={'request': request})
            return Response(output_serializer.data , status=status.HTTP_201_CREATED)
            
        except ContractAttachmentDomain.DoesNotExist:
                raise serializers.ValidationError("نوع پیوست یافت نشد")
        except Contract.DoesNotExist:
            return Response({"detail": " قراردادی با این آیدی یافت نشد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ساخت پیوست برای این  قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ContractAttachmentDetailsApiView(APIView):
    """
        GET: return an attachment of a Contract
        DELETE: delete an attachment of a Contract

        check object-level
        if user is superuser has access 
        else return only thoes check user has access to it via Contract
    """
    class ContractAttachmentDetailsOutputSerializer(serializers.ModelSerializer):
        class ContractAttachmentDetailsOutputSerializerUser(serializers.ModelSerializer): 
            class Meta:
                model = User
                fields = ['username' , 'first_name_fa' , 'last_name_fa']
        class ContractAttachmentDetailsOutputSerializerDtyp(serializers.ModelSerializer): 
            class Meta:
                model = ContractAttachmentDomain
                fields = ['id' , 'code', 'name_en', 'name_fa', 'typ']

        writer = ContractAttachmentDetailsOutputSerializerUser()
        dtyp = ContractAttachmentDetailsOutputSerializerDtyp()

        class Meta:
            model = ContractAttachment
            fields = ['id','upload_date','writer','contract','dtyp','file',]

    def get(self , request:Request , contractattachmentid:int)-> Response :
        try:
            user : User = request.user
            ContractAttachment_instance = ContractAttachment.objects.get(pk=contractattachmentid)
            if not user.is_superuser and not user.has_contract_access(ContractAttachment_instance.contract):
                return Response({"detail": "کاربر به  قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            serializer = self.ContractAttachmentDetailsOutputSerializer(ContractAttachment_instance,many=False,context={'request': request})
            return Response(serializer.data , status=status.HTTP_200_OK)
        except ContractAttachment.DoesNotExist:
            return Response({"detail": "پیوست  قراردادی با این آیدی یافت نشد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن پیوست  قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # def put ?????

    def delete(self , request:Request , contractattachmentid:int)-> Response :
        try:
            user : User = request.user
            ContractAttachment_instance = ContractAttachment.objects.get(pk=contractattachmentid)
            if not user.is_superuser and not user.has_contract_access(ContractAttachment_instance.contract):
                return Response({"detail": "کاربر به قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            ContractAttachment_instance.delete()
            delete_logger.warning(f"حذف پیوست  قرارداد {ContractAttachment_instance.file.path}" , extra=get_details_from_request(request))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ContractAttachment.DoesNotExist:
            return Response({"detail": "پیوست قراردادی با این آیدی یافت نشد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در حذف پیوست قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Shahrbase Attachment
class SharhbaseAttachmentDomainListApiView(SearchMixin, APIView):
    """
        List Of Sharhbase Attachment Domain`s
    """
    search_fields = ['code', 'name_en', 'name_fa', 'typ']

    class SharhbaseAttachmentDomainListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = SharhbaseAttachmentDomain
            fields = ['id', 'code', 'name_en', 'name_fa', 'typ']

    class SharhbaseAttachmentDomainListInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = SharhbaseAttachmentDomain
            fields = ['code', 'name_en', 'name_fa', 'typ']

    def get(self, request: Request) -> Response:
        try:
            all_SharhbaseAttachmentdomain = SharhbaseAttachmentDomain.objects.all()
            # Add Search query param to it
            all_SharhbaseAttachmentdomain = self.apply_search(all_SharhbaseAttachmentdomain, request)
            serializer = self.SharhbaseAttachmentDomainListOutputSerializer(
                all_SharhbaseAttachmentdomain,
                many=True,
                context={'request': request}
            )
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن انواع پیوست های بند شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request: Request) -> Response:
        try:
            input_serializer = self.SharhbaseAttachmentDomainListInputSerializer(data=request.data)
            if input_serializer.is_valid():
                shrh_instance = input_serializer.save()
                output_serializer = self.SharhbaseAttachmentDomainListOutputSerializer(shrh_instance)
                return Response(output_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ساخت نوع پیوست بند شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SharhbaseAttachmentDomainDetailsApiView(APIView):
    class SharhbaseAttachmentDomainDetailsOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = SharhbaseAttachmentDomain
            fields = ['id', 'code', 'name_en', 'name_fa', 'typ']

    class SharhbaseAttachmentDomainDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = SharhbaseAttachmentDomain
            fields = ['code', 'name_en', 'name_fa', 'typ']

    def get(self, request: Request, pk: int) -> Response:
        try:
            SharhbaseAttachmentdomain_instance = SharhbaseAttachmentDomain.objects.get(pk=pk)
            serializer = self.SharhbaseAttachmentDomainDetailsOutputSerializer(SharhbaseAttachmentdomain_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SharhbaseAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست بند شرح خدماتی با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن نوع پیوست بند شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request: Request, pk: int) -> Response:
        try:
            SharhbaseAttachmentdomain_instance = SharhbaseAttachmentDomain.objects.get(pk=pk)
            serializer = self.SharhbaseAttachmentDomainDetailsInputSerializer(
                SharhbaseAttachmentdomain_instance,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                # Save the updated instance
                updated_instance = serializer.save()
                output_serializer = self.SharhbaseAttachmentDomainDetailsOutputSerializer(updated_instance)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except SharhbaseAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست بند شرح خدماتی با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ویرایش نوع پیوست بند شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request: Request, pk: int) -> Response:
        try:
            SharhbaseAttachmentdomain_instance = SharhbaseAttachmentDomain.objects.get(pk=pk)
            SharhbaseAttachmentdomain_instance.delete()
            delete_logger.warning(f"حذف نوع پیوست بند شرح خدمات {SharhbaseAttachmentdomain_instance.name_fa}", extra=get_details_from_request(request))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SharhbaseAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست بند شرح خدماتی با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در حذف نوع پیوست بند شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SharhbaseAttachmentListApiView(SearchMixin, APIView):
    """
        GET: return all attachments of a ShrhBase
        POST: create new attachment of a ShrhBase

        check object-level
        if user is superuser has access
        else return only those checked user has access to via ShrhBase
    """
    search_fields = ['file', ]

    class SharhbaseAttachmentListOutputSerializer(serializers.ModelSerializer):
        class SharhbaseAttachmentListOutputSerializerUser(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ['username', 'first_name_fa', 'last_name_fa']

        class SharhbaseAttachmentListOutputSerializerDtyp(serializers.ModelSerializer):
            class Meta:
                model = SharhbaseAttachmentDomain
                fields = ['id', 'code', 'name_en', 'name_fa', 'typ']

        writer = SharhbaseAttachmentListOutputSerializerUser()
        dtyp = SharhbaseAttachmentListOutputSerializerDtyp()

        class Meta:
            model = SharhbaseAttachment
            fields = ['id', 'upload_date', 'writer', 'sharhbase', 'dtyp', 'file', ]

    class SharhbaseAttachmentListInputSerializer(serializers.Serializer):
        file = serializers.FileField(required=True, allow_null=False)
        dtyp_attach = serializers.IntegerField(required=True, allow_null=False)

        def validate_dtyp_attach(self, value):
            try:
                dtyp_attach_instance = SharhbaseAttachmentDomain.objects.get(pk=value)
                return value
            except SharhbaseAttachmentDomain.DoesNotExist:
                raise serializers.ValidationError("نوع پیوست یافت نشد")

    def get(self, request: Request, sharhbaseid: str) -> Response:
        try:
            user: User = request.user
            ShrhBase_instance = ShrhBase.objects.get(pk=sharhbaseid)
            if not user.is_superuser and not user.has_contract_access(ShrhBase_instance.contract):
                return Response({"detail": "کاربر به بند شرح خدمات دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)
            all_SharhbaseAttachments = SharhbaseAttachment.objects.filter(sharhbase=ShrhBase_instance)
            # Add Search query param to it
            all_SharhbaseAttachments = self.apply_search(all_SharhbaseAttachments, request)
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(all_SharhbaseAttachments, request)
            serializer = self.SharhbaseAttachmentListOutputSerializer(paginated_queryset, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        except ShrhBase.DoesNotExist:
            return Response({"detail": "بند شرح خدماتی با این آیدی یافت نشد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن پیوست های این بند شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request: Request, sharhbaseid: str) -> Response:
        try:
            user: User = request.user
            ShrhBase_instance = ShrhBase.objects.get(pk=sharhbaseid)
            if not user.is_superuser and not user.has_contract_access(ShrhBase_instance.contract):
                return Response({"detail": "کاربر به بند شرح خدمات دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)
            serializer = self.SharhbaseAttachmentListInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            validated_data = serializer.validated_data

            dtyp_attach_instance = SharhbaseAttachmentDomain.objects.get(pk=validated_data['dtyp_attach'])

            SharhbaseAttachment_instance = SharhbaseAttachment.objects.create(
                writer=request.user,
                sharhbase=ShrhBase_instance,
                dtyp=dtyp_attach_instance,
                file=validated_data['file'],
            )

            output_serializer = self.SharhbaseAttachmentListOutputSerializer(SharhbaseAttachment_instance, many=False, context={'request': request})
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except SharhbaseAttachmentDomain.DoesNotExist:
            raise serializers.ValidationError("نوع پیوست یافت نشد")
        except ShrhBase.DoesNotExist:
            return Response({"detail": "بند شرح خدماتی با این آیدی یافت نشد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ساخت پیوست برای این بند شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SharhbaseAttachmentDetailsApiView(APIView):
    """
        GET: return an attachment of a ShrhBase
        DELETE: delete an attachment of a ShrhBase

        check object-level
        if user is superuser has access
        else return only those checked user has access to via ShrhBase
    """
    class SharhbaseAttachmentDetailsOutputSerializer(serializers.ModelSerializer):
        class SharhbaseAttachmentDetailsOutputSerializerUser(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ['username', 'first_name_fa', 'last_name_fa']

        class SharhbaseAttachmentDetailsOutputSerializerDtyp(serializers.ModelSerializer):
            class Meta:
                model = SharhbaseAttachmentDomain
                fields = ['id', 'code', 'name_en', 'name_fa', 'typ']

        writer = SharhbaseAttachmentDetailsOutputSerializerUser()
        dtyp = SharhbaseAttachmentDetailsOutputSerializerDtyp()

        class Meta:
            model = SharhbaseAttachment
            fields = ['id', 'upload_date', 'writer', 'sharhbase', 'dtyp', 'file', ]

    def get(self, request: Request, sharhbaseid: int , sharhbaseattachmentid: int) -> Response:
        try:
            user: User = request.user
            SharhbaseAttachment_instance = SharhbaseAttachment.objects.get(pk=sharhbaseattachmentid)
            if not user.is_superuser and not user.has_contract_access(SharhbaseAttachment_instance.sharhbase.contract):
                return Response({"detail": "کاربر به بند شرح خدمات دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)
            serializer = self.SharhbaseAttachmentDetailsOutputSerializer(SharhbaseAttachment_instance, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SharhbaseAttachment.DoesNotExist:
            return Response({"detail": "پیوست بند شرح خدماتی با این آیدی یافت نشد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن پیوست بند شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def put ?????

    def delete(self, request: Request, sharhbaseid: int , sharhbaseattachmentid: int) -> Response:
        try:
            user: User = request.user
            SharhbaseAttachment_instance = SharhbaseAttachment.objects.get(pk=sharhbaseattachmentid)
            if not user.is_superuser and not user.has_contract_access(SharhbaseAttachment_instance.sharhbase.contract):
                return Response({"detail": "کاربر به بند شرح خدمات دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)
            SharhbaseAttachment_instance.delete()
            delete_logger.warning(f"حذف پیوست بند شرح خدمات {SharhbaseAttachment_instance.file.path}", extra=get_details_from_request(request))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SharhbaseAttachment.DoesNotExist:
            return Response({"detail": "پیوست بند شرح خدماتی با این آیدی یافت نشد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در حذف پیوست بند شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)