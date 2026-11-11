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
    Contract,
)
from contracts.models.attachment import(
    ContractAttachment,
    ContractAttachmentDomain,

)
from accounts.models import(
    User
)

delete_logger = logging.getLogger('delete_activity_logger')

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

