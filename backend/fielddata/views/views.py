# import uuid
# import json
# from datetime import date
# import logging
# from logs.utils import get_details_from_request
# from typing import cast, Dict, Any
# from django.core.validators import FileExtensionValidator
# from rest_framework.response import Response
# from rest_framework.request import Request
# from rest_framework import serializers
# from rest_framework.permissions import AllowAny , IsAdminUser
# from common.pagination import CustomPagination
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.urls import reverse
# from django.db import transaction
# from django.apps import apps
# from django.forms.models import model_to_dict   
# from django.contrib.gis.geos import MultiPolygon
# from django.core.exceptions import ValidationError

# from common.models import Company , Province
# from accounts.models import User

# from fielddata.models.models import (
#     ContractStep,
#     GeochemistaryFieldData,
# )
# from contracts.models.models import (
#     ContractDomin,
#     Contract,
#     ContractBorder
# )

# delete_logger = logging.getLogger('delete_activity_logger')
# api_activity_logger = logging.getLogger('api_activity_logger')



# class ContractStepListApiView(APIView):

#     class ContractStepListApiOutputSerializer(serializers.ModelSerializer):

#         class Meta:
#             model = ContractStep
#             fields = ["id","title"]

#     def get(self , request:Request , contractdomaincode : int) -> Response:
#         try:
#             related_contractdomain_instace : ContractDomin = ContractDomin.objects.get(code=contractdomaincode)

#             all_contractstep = ContractStep.objects.filter(dtyp=related_contractdomain_instace)

#             serializer = self.ContractStepListApiOutputSerializer(all_contractstep , many=True)
#             return Response(serializer.data , status=status.HTTP_200_OK)

#         except ContractDomin.DoesNotExist:
#             return Response({"detail": "نوع قراردادی با این کد یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

#         except Exception as e:
#             print(e)
#             return Response({"detail": "خطا در خواندن انواع قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# class GeochemistaryFieldDataListApiView(APIView):

#     class GeochemistaryFieldDataInputSerializer(serializers.ModelSerializer):
#         dstep = serializers.PrimaryKeyRelatedField(
#         queryset=ContractStep.objects.all(),
#         required=True,
#         error_messages={
#             'required': 'شناسه مرحله قرارداد الزامی است',
#             'does_not_exist': 'مرحله قرارداد با این شناسه یافت نشد',
#             'incorrect_type': 'نوع داده شناسه مرحله قرارداد نامعتبر است'
#         }
#         )
#         class Meta:
#             model = GeochemistaryFieldData
#             exclude = ['user' , 'contract' ,'created_at' , 'updated_at']

#     class GeochemistaryFieldDataOutputSerializer(serializers.ModelSerializer):
        
#         class GeochemistaryFieldDataOutputSerializerContract(serializers.ModelSerializer):
#             class Meta:
#                 model = Contract
#                 fields = ['id' , 'title']

#         class GeochemistaryFieldDataOutputSerializerUser(serializers.ModelSerializer):
#             class Meta:
#                 model = User
#                 fields = ['id' , 'username','first_name','last_name','first_name_fa','last_name_fa']

#         contract = GeochemistaryFieldDataOutputSerializerContract()
#         user = GeochemistaryFieldDataOutputSerializerUser()
#         class Meta:
#             model = GeochemistaryFieldData
#             fields = ["id" , "user" , "contract" , "created_at" , "updated_at" , "dstep"]


#     def get(self , request:Request , contractid : str) -> Response:
#         try:
#             user : User = request.user
            
#             # Fetch related objects
#             contract_instance = Contract.objects.get(pk=contractid)

#             # Check user permissions
#             if not user.is_superuser and not user.has_contract_access(contract_instance):
#                 return Response(
#                     {"detail": "کاربر به این قرارداد دسترسی ندارد"},
#                     status=status.HTTP_403_FORBIDDEN
#                 )
            
#             all_geochemistaryfielddata = GeochemistaryFieldData.objects.filter(contract=contract_instance)
#             serializer = self.GeochemistaryFieldDataOutputSerializer(all_geochemistaryfielddata, many=True)
#             return Response(serializer.data , status=status.HTTP_200_OK)

#         except Contract.DoesNotExist:
#             return Response(
#                 {"detail": "قراردادی با این شناسه یافت نشد"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         except Exception as e:
#             api_activity_logger.error(
#                 f"خطا در خواندن گزارش‌ های صحرایی ژیوشیمی این قرارداد: {str(e)}",
#                 extra=get_details_from_request(request)
#             )
#             return Response(
#                 {"detail": "خطا در خواندن گزارش‌ های صحرایی ژیوشیمی این قرارداد"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
    
#     def post(self , request:Request , contractid : str) -> Response:
#         try:
#             user : User = request.user
            
#             # Fetch related objects
#             contract_instance = Contract.objects.get(pk=contractid)

#             # Check user permissions
#             if not user.is_superuser and not user.has_contract_access(contract_instance):
#                 return Response(
#                     {"detail": "کاربر به این قرارداد دسترسی ندارد"},
#                     status=status.HTTP_403_FORBIDDEN
#                 )
            
#             # Validate and create
#             serializer = self.GeochemistaryFieldDataInputSerializer(data=request.data)
            
#             if not serializer.is_valid():
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#             dstep = serializer.validated_data.get('dstep')
#             print(dstep)

#             geochemistary_field_data = serializer.save(user=user, contract=contract_instance)
            
#             output_serializer = self.GeochemistaryFieldDataOutputSerializer(geochemistary_field_data)
#             return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        
#         except Contract.DoesNotExist:
#             return Response(
#                 {"detail": "قراردادی با این شناسه یافت نشد"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         except Exception as e:
#             api_activity_logger.error(
#                 f"خطا در ساخت گزارش‌ های صحرایی ژیوشیمی این قرارداد: {str(e)}",
#                 extra=get_details_from_request(request)
#             )
#             return Response(
#                 {"detail": "خطا در ساخت گزارش‌ های صحرایی ژیوشیمی این قرارداد"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


# class GeochemistaryFieldDataDetailsApiView(APIView):
#     class GeochemistaryFieldDataDetailsInputSerializer(serializers.ModelSerializer):
#         dstep = serializers.PrimaryKeyRelatedField(
#         queryset=ContractStep.objects.all(),
#         required=True,
#         error_messages={
#             'required': 'شناسه مرحله قرارداد الزامی است',
#             'does_not_exist': 'مرحله قرارداد با این شناسه یافت نشد',
#             'incorrect_type': 'نوع داده شناسه مرحله قرارداد نامعتبر است'
#         }
#         )
#         class Meta:
#             model = GeochemistaryFieldData
#             exclude = ['user' , 'contract' ,'created_at' , 'updated_at']

#     class GeochemistaryFieldDataDetailsOutputSerializer(serializers.ModelSerializer):
        
#         class GeochemistaryFieldDataDetailsOutputSerializerContract(serializers.ModelSerializer):
#             class Meta:
#                 model = Contract
#                 fields = ['id' , 'title']

#         class GeochemistaryFieldDataDetailsOutputSerializerUser(serializers.ModelSerializer):
#             class Meta:
#                 model = User
#                 fields = ['id' , 'username','first_name','last_name','first_name_fa','last_name_fa']

#         contract = GeochemistaryFieldDataDetailsOutputSerializerContract()
#         user = GeochemistaryFieldDataDetailsOutputSerializerUser()
#         class Meta:
#             model = GeochemistaryFieldData
#             fields = "__all__"

#     def get(self , request:Request , contractid : str , geochmfielddataid : int) -> Response:
#         try:
#             user : User = request.user

#             # Fetch related objects
#             contract_instance = Contract.objects.get(pk=contractid)

#             # Check user permissions
#             if not user.is_superuser and not user.has_contract_access(contract_instance):
#                 return Response(
#                     {"detail": "کاربر به این قرارداد دسترسی ندارد"},
#                     status=status.HTTP_403_FORBIDDEN
#                 )
            
#             geochemistaryfielddata_instace = GeochemistaryFieldData.objects.get(pk=geochmfielddataid)

#             if geochemistaryfielddata_instace.contract != contract_instance:
#                 return Response(
#                     {"detail": "قرارداد به این گزارش ارتباط ندارد"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             serializer = self.GeochemistaryFieldDataDetailsOutputSerializer(geochemistaryfielddata_instace)
#             return Response(serializer.data , status=status.HTTP_200_OK)

#         except GeochemistaryFieldData.DoesNotExist:
#             return Response(
#                 {"detail": "گزارش صحرایی ژیوشیمی با این شناسه یافت نشد"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         except Contract.DoesNotExist:
#             return Response(
#                 {"detail": "قراردادی با این شناسه یافت نشد"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         except Exception as e:
#             api_activity_logger.error(
#                 f"خطا در خواندن گزارش‌ های صحرایی ژیوشیمی این قرارداد: {str(e)}",
#                 extra=get_details_from_request(request)
#             )
#             return Response(
#                 {"detail": "خطا در خواندن گزارش‌ های صحرایی ژیوشیمی این قرارداد"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
        
#     def put(self , request:Request , contractid : str , geochmfielddataid : int) -> Response:
#         try:
#             user : User = request.user
            
#             # Fetch related objects
#             contract_instance = Contract.objects.get(pk=contractid)

#             # Check user permissions
#             if not user.is_superuser and not user.has_contract_access(contract_instance):
#                 return Response(
#                     {"detail": "کاربر به این قرارداد دسترسی ندارد"},
#                     status=status.HTTP_403_FORBIDDEN
#                 )
            
#             geochemistaryfielddata_instace = GeochemistaryFieldData.objects.get(pk=geochmfielddataid)

#             if geochemistaryfielddata_instace.contract != contract_instance:
#                 return Response(
#                     {"detail": "قرارداد به این گزارش ارتباط ندارد"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
            
#             # Validate and update
#             serializer = self.GeochemistaryFieldDataDetailsInputSerializer(
#                 geochemistaryfielddata_instace, 
#                 data=request.data
#             )
            
#             if not serializer.is_valid():
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
#             dstep = serializer.validated_data.get('dstep')
#             print(dstep)
                    
#             serializer.save(
#                 user=user
#             )
            
#             output_serializer = self.GeochemistaryFieldDataDetailsOutputSerializer(geochemistaryfielddata_instace)
#             return Response(output_serializer.data, status=status.HTTP_200_OK)

#         except GeochemistaryFieldData.DoesNotExist:
#             return Response(
#                 {"detail": "گزارش صحرایی ژیوشیمی با این شناسه یافت نشد"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         except Contract.DoesNotExist:
#             return Response(
#                 {"detail": "قراردادی با این شناسه یافت نشد"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         except Exception as e:
#             api_activity_logger.error(
#                 f"خطا در بروزرسانی گزارش‌ صحرایی ژیوشیمی این قرارداد: {str(e)}",
#                 extra=get_details_from_request(request)
#             )
#             return Response(
#                 {"detail": "خطا در بروزرسانی گزارش‌ صحرایی ژیوشیمی این قرارداد"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#     def delete(self , request:Request , contractid : str , geochmfielddataid : int) -> Response:
#         try:
#             user : User = request.user
                      
#             # Fetch related objects
#             contract_instance = Contract.objects.get(pk=contractid)

#             # Check user permissions
#             if not user.is_superuser and not user.has_contract_access(contract_instance):
#                 return Response(
#                     {"detail": "کاربر به این قرارداد دسترسی ندارد"},
#                     status=status.HTTP_403_FORBIDDEN
#                 )
            
#             geochemistaryfielddata_instace = GeochemistaryFieldData.objects.get(pk=geochmfielddataid)

#             if geochemistaryfielddata_instace.contract != contract_instance:
#                 return Response(
#                     {"detail": "قرارداد به این گزارش ارتباط ندارد"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
            
#             delete_logger.warning(f"حذف گزارش صحرایی ژیوشیمی قرارداد {contract_instance.title}" , extra=get_details_from_request(request))
#             geochemistaryfielddata_instace.delete()

#             return Response(status=status.HTTP_204_NO_CONTENT)

#         except GeochemistaryFieldData.DoesNotExist:
#             return Response(
#                 {"detail": "گزارش صحرایی ژیوشیمی با این شناسه یافت نشد"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         except Contract.DoesNotExist:
#             return Response(
#                 {"detail": "قراردادی با این شناسه یافت نشد"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         except Exception as e:
#             api_activity_logger.error(
#                 f"خطا در حذف گزارش‌ صحرایی ژیوشیمی این قرارداد: {str(e)}",
#                 extra=get_details_from_request(request)
#             )
#             return Response(
#                 {"detail": "خطا در حذف گزارش‌ صحرایی ژیوشیمی این قرارداد"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

    
