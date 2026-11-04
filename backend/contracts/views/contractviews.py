import os
import logging
from datetime import datetime
from logs.utils import get_details_from_request
from typing import cast, Dict, Any
from django.core.validators import FileExtensionValidator
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import serializers
from django.conf import settings
from rest_framework.permissions import AllowAny , IsAdminUser
from common.pagination import CustomPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from django.db import transaction
from django.contrib.gis.geos import MultiPolygon

from common.services.gis import queryset_to_shapefile
from common.models import Company , Province
from common.mixins import SearchMixin
from accounts.models import User
from initialborders.models.models import (
    InitialBorder,
    InitialBorderDomin
)

from contracts.models.models import (
    ContractDomin,
    Contract,
    ContractElhaghye,
    ContractBorder
)

from contracts.services.gis import(
    process_contractborder
)

delete_logger = logging.getLogger('delete_activity_logger')

class ContractListApiViews(SearchMixin , APIView):
    """ 
    GET: List of all Contract`s

    if user is superuser return all 
    else return only thoes contracts this user has access
    """
    # look at SearchMixin its come from there !
    search_fields = ['title' ,'dtyp__title','number',]

    class ContractListOutputSerializer(serializers.ModelSerializer):
        class ContractListDtypSerializer(serializers.ModelSerializer):
            class Meta:
                model = ContractDomin
                fields = ['id','title','code']
        dtyp = ContractListDtypSerializer()
        class Meta:
            model = Contract
            fields = [
                'id','title', 'dtyp', 'number', 'start_date', 'end_date', 
                'progress', 'is_completed', 'department', 
                'mablagh','company'
                ]

    class ContractListInputSerializer(serializers.ModelSerializer):
        department = serializers.ChoiceField(
            choices=Contract.DEPARTMENT_CHOICES,
            required=False,
            allow_null=True,
            allow_blank=True,
            error_messages={
                'invalid_choice': f'انتخاب نامعتبر است. گزینه‌های معتبر: {", ".join([f"{choice[0]} ({choice[1]})" for choice in Contract.DEPARTMENT_CHOICES])}'
            }
        )
        company = serializers.PrimaryKeyRelatedField(
            many=True,
            queryset=Company.objects.all(),
            error_messages={
                'does_not_exist': 'شرکت با شناسه "{pk_value}" یافت نشد.',
                'incorrect_type': 'مقدار نامعتبر برای شناسه شرکت: باید عدد باشد.'
            }
        )
   
        class Meta:
            model = Contract
            fields = [
                'title', 'dtyp', 'number', 'start_date', 'end_date', 
                'progress', 'is_completed', 'department', 
                'mablagh','company'
                ]
            extra_kwargs = {
                'department': {'required': False},
                'elhaghye': {'required': False},
                }

    def get(self , request:Request) -> Response:
        try:
            user : User = request.user
            if user.is_superuser:
                all_contract = Contract.objects.all()
            else:
                all_contract = user.get_accessible_contracts()

            # Add Search query param to it
            all_contract = self.apply_search(all_contract, request)

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(all_contract, request)
            serializer = self.ContractListOutputSerializer(paginated_queryset,many=True,context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن لیست قراردادها"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self , request:Request) -> Response:
        """
            POST: 
                1. Create a Contract Instance
                2. Grant aceess to this user who create this Contract automatically
        """
        try:
            user : User = request.user
            serializer = self.ContractListInputSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = cast(Dict[str, Any], serializer.validated_data)
                with transaction.atomic():
                    contract = serializer.save()
                    user.grant_contract_access(contract=contract)
                # Return the created contract data
                output_serializer = self.ContractListOutputSerializer(contract, context={'request': request})
                return Response(output_serializer.data, status=status.HTTP_201_CREATED)               
            else:
                #setializer have error
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ایجاد قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        

class ContractDetailsApiViews(APIView):
    """
        - Get: Retrive a Contract By id
        - Put: Partial Update the contract 
            (can update contractborder via ziped shape file too (old contractborder`s of a contract deleted) )
        - Delete: find a Contract by id and delete it 

        - Object-level check
        if user is superuser has access 
        else return only thoes check user has access to it via
        shrhlayer -> sharhbase -> contract
    """

    class ContractDetailsOutputSerializer(serializers.ModelSerializer):
        class ContractDetailsDtypSerializer(serializers.ModelSerializer):
            class Meta:
                model = ContractDomin
                fields = ['id','title','code']
        class ContractDetailsInitialBorderSerializer(serializers.ModelSerializer):
            class ContractDetailsInitialBorderDomainSerializer(serializers.ModelSerializer):
                class Meta:
                    model = InitialBorderDomin
                    fields = ['id','title','code']
            dtyp = ContractDetailsInitialBorderDomainSerializer()
            class Meta:
                model = InitialBorder
                fields = ['id' , 'title' , 'dtyp']
        class ContractDetailsCompanySerializer(serializers.ModelSerializer):
            class Meta:
                model = Company
                fields = ['id','name','typ','service_typ','code']
        dtyp = ContractDetailsDtypSerializer()
        contractborders = serializers.PrimaryKeyRelatedField(many=True,read_only=True,source='rcontractborders')
        company=ContractDetailsCompanySerializer(many=True)
        class Meta: 
            model = Contract
            fields = ['id','title','dtyp','number','progress','company',
                    'is_completed','department','start_date','end_date','elhaghye','contractborders']
  
    class ContractDetailsInputSerializer(serializers.ModelSerializer):
        department = serializers.ChoiceField(
            choices=Contract.DEPARTMENT_CHOICES,
            required=False,
            allow_null=True,
            allow_blank=True,
            error_messages={
                'invalid_choice': f'انتخاب نامعتبر است. گزینه‌های معتبر: {", ".join([f"{choice[0]} ({choice[1]})" for choice in Contract.DEPARTMENT_CHOICES])}'
            }
        )
   
        class Meta:
            model = Contract
            fields = [   
                'title', 'dtyp', 'number', 'start_date', 'end_date', 
                'progress', 'is_completed', 'department', 
                'mablagh','company'
                ]

    def get(self , request:Request , contractid:str) -> Response:
        try:
            user : User = request.user
            contract_instance = Contract.objects.get(pk=contractid)
            if not user.is_superuser and not user.has_contract_access(contract_instance):
                return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            serializer = self.ContractDetailsOutputSerializer(contract_instance)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except Contract.DoesNotExist:
            return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن قراردادی با این آیدی"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self , request:Request , contractid:str) -> Response:
        try:
            user : User = request.user
            contract_instance = Contract.objects.get(pk=contractid)
            if not user.is_superuser and not user.has_contract_access(contract_instance):
                return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            serializer = self.ContractDetailsInputSerializer(
                contract_instance, 
                data=request.data, 
                partial=True  # Allow partial updates
            )
            if serializer.is_valid():
                validated_data = cast(Dict[str, Any], serializer.validated_data)
                updated_contract = serializer.save()
                # Return the updated contract data
                output_serializer = self.ContractDetailsOutputSerializer(updated_contract, context={'request': request})
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else: #serializer error
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        except Contract.DoesNotExist:
            return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ویرایش قراردادی با این آیدی"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self , request:Request , contractid:str) -> Response:
        try:
            user : User = request.user
            contract_instance = Contract.objects.get(pk=contractid)
            if not user.is_superuser and not user.has_contract_access(contract_instance):
                return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            contract_instance.delete()
            delete_logger.warning(f"حذف قرارداد {contract_instance.title}" , extra=get_details_from_request(request))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Contract.DoesNotExist:
            return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در حذف قراردادی با این آیدی"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ContractElhaghyeListApiViews(APIView):
    class ContractElhaghyeOutputSerializer(serializers.ModelSerializer):

        class Meta:
            model = ContractElhaghye
            fields = ['pk', 'contract' , 'title' , 'mablagh' , 'tarikh' , 'description']

    class ContractElhaghyeInputSerializer(serializers.ModelSerializer):

        class Meta:
            model = ContractElhaghye
            fields = ['title' , 'mablagh' , 'tarikh' , 'description']


    def get(self , request:Request , contractid:str):
        try:
            user : User = request.user
            contract_instance = Contract.objects.get(pk=contractid)
            if not user.is_superuser and not user.has_contract_access(contract_instance):
                return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            
            all_contractelhaghye = ContractElhaghye.objects.filter(contract=contract_instance)
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(all_contractelhaghye, request)
            serializer = self.ContractElhaghyeOutputSerializer(paginated_queryset,many=True,context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        except Contract.DoesNotExist:
            return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن الحاقیع قراردادی با این آیدی"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request: Request, contractid: str):
        try:
            user: User = request.user
            contract_instance = Contract.objects.get(pk=contractid)
            if not user.is_superuser and not user.has_contract_access(contract_instance):
                return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.ContractElhaghyeInputSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = cast(Dict[str, Any], serializer.validated_data)
                contractelhaghye = serializer.save(contract=contract_instance)
                output_serializer = self.ContractElhaghyeOutputSerializer(contractelhaghye, context={'request': request})
                return Response(output_serializer.data, status=status.HTTP_201_CREATED)
            else:
                # serializer have error
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Contract.DoesNotExist:
            return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ساخت الحاقیه قراردادی با این آیدی"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ContractElhaghyeDetailsApiViews(APIView):
    """
        - Get: Retrive a ContractElhaghye By id
        - Put: Partial Update the contract elhaghye
        - Delete: find a ContractElhaghye by id and delete it 

        - Object-level check
        if user is superuser has access 
        else return only thoes check user has access to it via has_contract_access
    """

    class ContractElhaghyeOutputSerializer(serializers.ModelSerializer):

        class Meta:
            model = ContractElhaghye
            fields = ['pk', 'contract', 'title', 'mablagh', 'tarikh', 'description']

    class ContractElhaghyeInputSerializer(serializers.ModelSerializer):

        class Meta:
            model = ContractElhaghye
            fields = ['title', 'mablagh', 'tarikh', 'description']

    def get(self, request: Request, contractid: str, id: str) -> Response:
        try:
            user: User = request.user
            contract_instance = Contract.objects.get(pk=contractid)
            if not user.is_superuser and not user.has_contract_access(contract_instance):
                return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            elhaghye_instance = ContractElhaghye.objects.get(pk=id, contract=contract_instance)
            serializer = self.ContractElhaghyeOutputSerializer(elhaghye_instance, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Contract.DoesNotExist:
            return Response({"detail": "قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)
        except ContractElhaghye.DoesNotExist:
            return Response({"detail": "الحاقیه‌ای با این آیدی برای این قرارداد وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن الحاقیه قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request: Request, contractid: str, id: str) -> Response:
        try:
            user: User = request.user
            contract_instance = Contract.objects.get(pk=contractid)
            if not user.is_superuser and not user.has_contract_access(contract_instance):
                return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            elhaghye_instance = ContractElhaghye.objects.get(pk=id, contract=contract_instance)
            serializer = self.ContractElhaghyeInputSerializer(
                elhaghye_instance,
                data=request.data,
                partial=True  # Allow partial updates
            )
            if serializer.is_valid():
                validated_data = cast(Dict[str, Any], serializer.validated_data)
                updated_elhaghye = serializer.save()
                output_serializer = self.ContractElhaghyeOutputSerializer(updated_elhaghye, context={'request': request})
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else:  # serializer error
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Contract.DoesNotExist:
            return Response({"detail": "قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)
        except ContractElhaghye.DoesNotExist:
            return Response({"detail": "الحاقیه‌ای با این آیدی برای این قرارداد وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ویرایش الحاقیه قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request: Request, contractid: str, id: str) -> Response:
        try:
            user: User = request.user
            contract_instance = Contract.objects.get(pk=contractid)
            if not user.is_superuser and not user.has_contract_access(contract_instance):
                return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"}, status=status.HTTP_403_FORBIDDEN)

            elhaghye_instance = ContractElhaghye.objects.get(pk=id, contract=contract_instance)
            elhaghye_instance.delete()
            delete_logger.warning(f"حذف الحاقیه قرارداد {contract_instance.title}", extra=get_details_from_request(request))
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Contract.DoesNotExist:
            return Response({"detail": "قراردادی با این آیدی وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)
        except ContractElhaghye.DoesNotExist:
            return Response({"detail": "الحاقیه‌ای با این آیدی برای این قرارداد وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در حذف الحاقیه قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContractBorderListApiView(SearchMixin , APIView):
    """
        Get: list of all contractborders
        ?initilaborder=<id> filter only this related to this initialborder
        ?contract=<id> filter only this related to this contract

        POST: Create a new Contract border for a contract & Initborder
        the titile and scale of a border must be in shape file
        
        in shape rows ==> <titile> <scale> <border>
        create new contractborder instance for every row related to contract & Initborder
    """
    
    # add more fields whenever you need
    search_fields = ['title']  
    class ContractBorderListOutputSeializer(serializers.ModelSerializer):

        class ContractBorderListOutputSeializerContract(serializers.ModelSerializer):
            class Meta:
                model = Contract
                fields = ['id','title','number','start_date','end_date','is_completed']
        
        class ContractBorderListOutputSeializerInitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorder
                fields = ['id','title']

        contract = ContractBorderListOutputSeializerContract()
        initborder = ContractBorderListOutputSeializerInitialborder()
        class Meta:
            model = ContractBorder
            fields = ['id' , 'title' , 'scale' , 'center' , 'bbox' , 'initborder' , 'contract' ,]

    class ContractBorderListInputSerializer(serializers.Serializer):
        file = serializers.FileField(
            required=True,
            allow_null=True,
            error_messages={
                "required":"این فیلد اجباری است",
            },
            validators=[
            FileExtensionValidator(
                allowed_extensions=['zip'],
                message="فایل محدوده حتما باید با فرمت zip باشد"
            )
        ])
        initialborder = serializers.PrimaryKeyRelatedField(
            queryset=InitialBorder.objects.all(),
            error_messages={
                "required":"این فیلد اجباری است",
                "does_not_exist": "محدوده اولیه با این آیدی یافت نشد",
                "incorrect_type": "نوع آیدی محدوده اولیه معتبر نمیباشد"
            }
        )
        contract = serializers.PrimaryKeyRelatedField(
            queryset=Contract.objects.all(),
            error_messages={
                "required":"این فیلد اجباری است",
                "does_not_exist": "قراردادی با این آیدی یافت نشد",
                "incorrect_type": "نوع آیدی قرارداد معتبر نمیباشد"
            }
        )
            
        def validate_file(self, value):
            # Check file size
            max_size = 100 * 1024 * 1024  # 100 MB
            if value.size > max_size:
                raise serializers.ValidationError("File size cannot exceed 100 MB.")
            return value

    def _build_filters(self, request: Request) -> dict:
        """Build filter dictionary from query params"""
        filters = {}
        
        # Add initialborder filter if provided
        initialborderid_param = request.query_params.get('initialborder')
        if initialborderid_param:
            try:
                filters['initborder_id'] = int(initialborderid_param) if initialborderid_param.isdigit() else initialborderid_param
            except ValueError:
                raise ValueError({"initialborder": "شناسه محدوده اولیه معتبر نیست"})
        
        # Add contract filter if provided
        contractid_param = request.query_params.get('contract')
        if contractid_param:
            # Assuming contract_id is UUID
            filters['contract_id'] = contractid_param
        
        return filters

    def get(self , request:Request) -> Response:
        try:
            user : User = request.user

            if user.is_superuser:
                all_contractborders = ContractBorder.objects.all()
            else:
                all_contractborders = user.get_accessible_contractborders()

            # Build and apply filters
            filters = self._build_filters(request)
            if filters:
                all_contractborders = all_contractborders.filter(**filters)

            # Add search field as query param
            all_contractborders = self.apply_search(all_contractborders, request)

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(all_contractborders, request)
            serializer = self.ContractBorderListOutputSeializer(paginated_queryset,many=True,context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن لیست محدوده قراردادها"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self , request:Request) -> Response:
        user : User  = request.user
        serializer = self.ContractBorderListInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validated_data = cast(Dict[str, Any], serializer.validated_data)

            zip_file = validated_data.pop('file')
            res , result_data , message = process_contractborder(zipfile_obj=zip_file)
            if not res:
                return Response({"detail":message} , status=status.HTTP_400_BAD_REQUEST)
            
            """
            Check title uniquenes with 
            already existing Contractborder instance in DataBase
            """
            for resd in result_data:
                if ContractBorder.objects.filter(title=resd['title'],contract=validated_data['contract']).exists():
                    return Response({"detail":f"محدوده قراردادی با عنوان {resd['title']} از قبل برای این قرارداد وجود دارد"} , status=status.HTTP_400_BAD_REQUEST)
                
            if len(result_data)>50:
                return Response({"detail":"تعداد محدوده‌های قرارداد بیششتر از ۵۰ تا است"} , status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():
                contract_borders = []
                for res in result_data:
                    # Convert single polygon to MultiPolygon for the model field
                    border = MultiPolygon(res['border'])
                    contract_border = ContractBorder.objects.create(
                        initborder=validated_data['initialborder'] ,
                        contract=validated_data['contract'] ,
                        border=border,
                        scale=res['scale'], # May have value or None !
                        title=res['title'],
                    )
                    contract_borders.append(contract_border)

                user.grant_bulk_contractborder_access(contractborders=contract_borders)
        
            # Return the created contract data
            output_serializer = self.ContractBorderListOutputSeializer(contract_borders,many=True , context={'request': request})
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ساخت محدوده قرارداد جدید"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ContractBorderDetailsApiView(APIView):
    """
        GET: Retrive ContractBorder with all realated fileds
        PUT: Edit only one contractborder instance
        DELETE: Remove a ContractBorder Instance

        check object-level
        if user is superuser has access 
        else return only thoes check user has access to it via
        shrhlayer -> contractborder
    """

    class ContractBorderDetailsOutputSerializer(serializers.ModelSerializer):
        class ContractBorderDetailsOutputSerializerContract(serializers.ModelSerializer):
            class ContractBorderDetailsOutputSerializerContractDomain(serializers.ModelSerializer):
                class Meta:
                    model = ContractDomin
                    fields = ['id','title','code']
            dtyp = ContractBorderDetailsOutputSerializerContractDomain()
            class Meta:
                model = Contract
                fields = ['id','title','dtyp','number']
        class ContractBorderDetailsOutputSerializerInitborder(serializers.ModelSerializer):
            class ContractBorderDetailsOutputSerializerInitborderProvince(serializers.ModelSerializer):
                class Meta:
                    model = Province
                    fields = ['id','name_fa','cnter_name_fa','code']
            class ContractBorderDetailsOutputSerializerInitborderDomin(serializers.ModelSerializer):
                class Meta:
                    model = InitialBorderDomin
                    fields = ['id' , 'title' , 'code']
            province = ContractBorderDetailsOutputSerializerInitborderProvince(many=True)
            dtyp = ContractBorderDetailsOutputSerializerInitborderDomin()
            class Meta:
                model = InitialBorder
                fields = ['id','title','dtyp','center','bbox','parentid','province',]

        contract = ContractBorderDetailsOutputSerializerContract()
        initborder = ContractBorderDetailsOutputSerializerInitborder()

        class Meta:
            model = ContractBorder
            fields = ['id' , 'title' , 'scale' ,'center','bbox', 'initborder' , 'contract']

    class ContractBorderDetailsInputSerializer(serializers.Serializer):
        file = serializers.FileField(
            required=False,
            allow_null=True,
            validators=[
            FileExtensionValidator(
                allowed_extensions=['zip'],
                message="فایل محدوده حتما باید با فرمت zip باشد"
            )
        ])
        initialborder = serializers.IntegerField(
            required=False,
            allow_null=True,
        )

        def validate_initialborder(self, value):
            if value is not None:  # Changed from 'if value'
                try:
                    init_border_instance = InitialBorder.objects.get(pk=value)
                    return init_border_instance  # Return the instance
                except InitialBorder.DoesNotExist:
                    raise serializers.ValidationError("محدوده اولیه ایی با این آیدی یافت نشد")  # Use serializers.ValidationError
            return value  # Return None if not provided

    def get(self , request:Request , pk:str) -> Response:
        try:
            user : User = request.user
            contractborder_instance = ContractBorder.objects.get(pk=pk)
            if not user.is_superuser and not user.has_contractborder_access(contractborder_instance):
                return Response({"detail": "کاربر به محدوده قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            serializer = self.ContractBorderDetailsOutputSerializer(contractborder_instance)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except ContractBorder.DoesNotExist:
            return Response({"detail": "محدوده قراردادی با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن محدوده قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self , request:Request , pk:str) -> Response:
        try:
            user : User = request.user

            contractborder_instance = ContractBorder.objects.get(pk=pk)
            if not user.is_superuser and not user.has_contractborder_access(contractborder_instance):
                return Response({"detail": "کاربر به محدوده قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            
            serializer = self.ContractBorderDetailsInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = cast(Dict[str, Any], serializer.validated_data)
            
            zip_file = validated_data.get('file')
            if zip_file:
                res , result_data , message = process_contractborder(zipfile_obj=zip_file)
                
                if len(result_data)>1:
                    return Response({"detail":"برای تغییر محدوده این محدوده قرارداد باید حتما یک محدوده در شیپ فایل وارد شده باشد"} , status=status.HTTP_400_BAD_REQUEST)
                if not res:
                    return Response({"detail":message} , status=status.HTTP_400_BAD_REQUEST)
                
                #check title change
                if contractborder_instance.title != result_data[0]['title']:
                    #check another contractborder in this contract have the same title
                    if ContractBorder.objects.filter(title=result_data[0]['title'],contract=contractborder_instance.contract).exists():
                        return Response({"detail":f"محدوده قراردادی با عنوان {result_data[0]['title']} از قبل برای این قرارداد وجود دارد"} , status=status.HTTP_400_BAD_REQUEST)
                    
                contractborder_instance.title = result_data[0]['title']
                contractborder_instance.border = MultiPolygon(result_data[0]['border'])
                contractborder_instance.scale = result_data[0]['scale']
                # contractborder_instance.save()

            # Handle InitialBorder update (works independently of file upload)
            new_initialborder = validated_data.get('initialborder')
            if new_initialborder is not None:  # Check for None instead of truthy
                contractborder_instance.initborder = new_initialborder
        
            # Save once after all changes
            contractborder_instance.save()

            serializer = self.ContractBorderDetailsOutputSerializer(contractborder_instance)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except ContractBorder.DoesNotExist:
            return Response({"detail": "محدوده قراردادی با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ویرایش محدوده قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self , request:Request , pk:str) -> Response:
        try:
            user : User = request.user
            contractborder_instance = ContractBorder.objects.get(pk=pk)
            if not user.is_superuser and not user.has_contractborder_access(contractborder_instance):
                return Response({"detail": "کاربر به محدوده قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            
            contractborder_instance.delete()
            delete_logger.warning(f"حذف محدوده قرارداد {contractborder_instance.title}" , extra=get_details_from_request(request))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ContractBorder.DoesNotExist:
            return Response({"detail": "محدوده قراردادی با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در حذف محدوده قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ContractBorderDownloadExportShapeApiViews(APIView):
    def post(self ,  request:Request , pk:int) -> Response:
        try:
            user : User = request.user
            contractborder_instance = ContractBorder.objects.get(pk=pk)
            if not user.is_superuser and not user.has_contractborder_access(contractborder_instance):
                return Response({"detail": "کاربر به محدوده قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            
            queryset = ContractBorder.objects.filter(pk=pk)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            zip_path = queryset_to_shapefile(
                queryset=queryset,
                geometry_field="border",
                zip_output=True,
                filename=f"contractborder_{pk}_{timestamp}",
            )

            # ── Build download URL from the absolute path ──────────────
            relative_path = os.path.relpath(zip_path, settings.MEDIA_ROOT)
            download_url = request.build_absolute_uri(
                f"{settings.MEDIA_URL}{relative_path}"
            )


            return Response(
                {
                    "detail": "شیپ فایل با موفقیت ایجاد شد",
                    "download_url": download_url,
                },
                status=status.HTTP_200_OK,
            )
            

        except ContractBorder.DoesNotExist:
            return Response({"detail": "محدوده قراردادی با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ساخت خروجی شیپ محدوده قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AllContractBorderDownloadExportShapeApiViews(APIView):
    def post(self ,  request:Request) -> Response:
        try:
            user : User = request.user
            all_contractborder_instances = ContractBorder.objects.all()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            zip_path = queryset_to_shapefile(
                queryset=all_contractborder_instances,
                geometry_field="border",
                zip_output=True,
                filename=f"allcontractborder_{timestamp}",
            )

            # ── Build download URL from the absolute path ──────────────
            relative_path = os.path.relpath(zip_path, settings.MEDIA_ROOT)
            download_url = request.build_absolute_uri(
                f"{settings.MEDIA_URL}{relative_path}"
            )

            return Response(
                {
                    "detail": "شیپ فایل با موفقیت ایجاد شد",
                    "download_url": download_url,
                },
                status=status.HTTP_200_OK,
            )
            
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ساخت خروجی شیپ همه محدوده قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ContractDomainsListApiView(APIView):
    """
        Get: List of all contract domians
        Post: Contract domain connect to layername so user must not create it
    """
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            # For GET requests, allow any user
            return [AllowAny()]
        else:
            # For all other methods (POST, PUT, PATCH, DELETE), require admin
            return [IsAdminUser()]
        
    class ContractDomainsListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ContractDomin
            fields = ['id','title','code']

    def get(self , request:Request) -> Response:
        try:
            all_contractdomains = ContractDomin.objects.all()
            serializer = self.ContractDomainsListOutputSerializer(all_contractdomains , many=True)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن انواع قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)