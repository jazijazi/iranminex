import logging
from logs.utils import get_details_from_request
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import exceptions , status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from common.pagination import CustomPagination
from common.mixins import SearchMixin

from common.models import Company
from accounts.models import (
    User,
    Apis,
    Tools,
    Roles,
)
from contracts.models.models import (
    Contract,
    ContractBorder
)
from contracts.models.SharhKhadamats import ShrhLayer
from initialborders.models.models import InitialBorder

delete_logger = logging.getLogger('delete_activity_logger')
user_activity_logger = logging.getLogger('user_activity_logger')


class UserManagementListApiView(SearchMixin, APIView):
    """
        GET: Return List of All Users
        POST: Create a New User
    """
    permission_classes = [IsAdminUser]
    search_fields = ['username','first_name_fa','last_name_fa',
                     'first_name','last_name','email','phonenumber','codemeli',]

    class UserManagementListOutputSerializer(serializers.ModelSerializer):
        class UserManagementListOutputRoles(serializers.ModelSerializer):
            class Meta:
                model = Roles
                fields = ['id','title']
        class UserManagementListOutputCompany(serializers.ModelSerializer):
            class Meta:
                model = Company
                fields = ['id','name','typ','service_typ','code']
        roles = UserManagementListOutputRoles()
        company = UserManagementListOutputCompany()
        class Meta:
            model = User
            fields = ['id','username','first_name_fa','last_name_fa','address',
                      'accessible_shrh_layers',
                      'accessible_contracts',
                      'accessible_initialborders',
                      'first_name','last_name','email','is_staff','is_active','is_controller',
                      'phonenumber','codemeli','fax','start_access','end_access',
                      'date_joined','last_login','is_active','roles','company']
            
    class UserManagementListInputSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True, min_length=8)
        confirm_password = serializers.CharField(write_only=True)
        
        accessible_shrh_layers = serializers.ListField(
            child=serializers.IntegerField(),
            required=False,
            allow_empty=True,
        )
        accessible_contracts = serializers.ListField(
            child=serializers.UUIDField(),
            required=False,
            allow_empty=True,
        )
        accessible_initialborders = serializers.ListField(
            child=serializers.IntegerField(),
            required=False,
            allow_empty=True,
        )

        def validate_accessible_shrh_layers(self, value):
            """
            Validate that all provided ShrhLayer IDs exist
            """
            if value:
                from contracts.models.SharhKhadamats import ShrhLayer
                existing_ids = ShrhLayer.objects.filter(id__in=value).values_list('id', flat=True)
                invalid_ids = set(value) - set(existing_ids)
                
                if invalid_ids:
                    raise serializers.ValidationError(
                        f"لایه‌های با شناسه‌های {list(invalid_ids)} یافت نشدند"
                    )
            return value
        
        def validate_accessible_contracts(self, value):
            """
            Validate that all provided Contract IDs exist
            """
            if value:
                existing_ids = Contract.objects.filter(id__in=value).values_list('id', flat=True)
                invalid_ids = set(value) - set(existing_ids)
                
                if invalid_ids:
                    raise serializers.ValidationError(
                        f"قراردادهای با شناسه‌های {list(invalid_ids)} یافت نشدند"
                    )
            return value
        
        
        def validate_accessible_initialborders(self, value):
            """
            Validate that all provided InitialBorder IDs exist
            """
            if value:
                existing_ids = InitialBorder.objects.filter(id__in=value).values_list('id', flat=True)
                invalid_ids = set(value) - set(existing_ids)
                
                if invalid_ids:
                    raise serializers.ValidationError(
                        f"محدوده‌های اولیه با شناسه‌های {list(invalid_ids)} یافت نشدند"
                    )
            return value

        def validate_password(self, password):
            """
            Validate password using Django's password validators from settings
            """
            try:
                # This will use your CustomPasswordValidator from settings
                validate_password(password)
            except DjangoValidationError as e:
                # Convert Django validation errors to DRF format
                raise serializers.ValidationError(e.messages)
            return password
        def validate(self, attrs):
            """
            Validate that password and confirm_password match
            """
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            
            if password != confirm_password:
                raise serializers.ValidationError({
                    'confirm_password': 'رمز عبور و تکرار آن باید یکسان باشند'
                })
            
            # Remove confirm_password from validated data as it's not needed for saving
            attrs.pop('confirm_password', None)
            return attrs
        def create(self, validated_data):
            """
            Create user with hashed password
            """
            # Extract permission lists before creating user
            accessible_shrh_layers = validated_data.pop('accessible_shrh_layers', [])
            accessible_contracts = validated_data.pop('accessible_contracts', [])
            accessible_initialborders = validated_data.pop('accessible_initialborders', [])
            
            # Hash the password before saving
            password = validated_data.get('password')
            if password:
                validated_data['password'] = make_password(password)
            
            user = super().create(validated_data)

            if accessible_shrh_layers:
                layers = ShrhLayer.objects.filter(id__in=accessible_shrh_layers)
                user.grant_bulk_sharhlayer_access(list(layers))
            
            if accessible_contracts:
                contracts = Contract.objects.filter(id__in=accessible_contracts)
                user.grant_bulk_contract_access(list(contracts))
            
            if accessible_initialborders:
                initialborders = InitialBorder.objects.filter(id__in=accessible_initialborders)
                user.grant_bulk_initialborder_access(list(initialborders))

            return user
            
        class Meta:
            model = User
            fields = ['username','first_name_fa','last_name_fa','address','is_controller',
                      'accessible_shrh_layers',
                      'accessible_contracts',
                      'accessible_initialborders',
                      'first_name','last_name','email','roles',
                      'phonenumber','codemeli','fax','start_access','end_access',
                      'password','confirm_password','company']
    
            

    def get(self, request: Request) -> Response:
        try:
            all_users = User.objects.all()
            # Add Search query param to it
            all_users = self.apply_search(all_users, request)
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(all_users, request)
            serializer = self.UserManagementListOutputSerializer(paginated_queryset , many=True)

            user_activity_logger.info(f"دریافت لیست کامل کاربرها" , extra=get_details_from_request(request))
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:                      
            user_activity_logger.error(f"خطا در دریافت لیست کامل کاربرها  {str(e)}" , extra=get_details_from_request(request))
            return Response(
                {"detail": "خطا در خواندن لیست کاربر ها"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def post(self, request:Request) -> Response:
        try:
            serializer = self.UserManagementListInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            
            # Return the created user data using output serializer
            output_serializer = self.UserManagementListOutputSerializer(user)

            user_activity_logger.warning(f"کاربر جدید {user.username} با موفقیت ساخته شد" , extra=get_details_from_request(request))
            return Response(output_serializer.data,status=status.HTTP_201_CREATED)
            
        except Exception as e:                      
            user_activity_logger.error(f"خطا در ساخت کاربر جدید {str(e)}" , extra=get_details_from_request(request))
            return Response(
                {"detail": "خطا در ساخت کاربر جدید"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class UserManagementDetailsApiView(APIView):
    """
        GET: Return List of All Users
        POST: Create a New User
    """
    permission_classes = [IsAdminUser]

    class UserManagementtDetailsOutputSerializer(serializers.ModelSerializer):
        class UserManagementtDetailsOutputRoles(serializers.ModelSerializer):
            class Meta:
                model = Roles
                fields = ['id','title']
        class UserManagementDetailsOutputCompany(serializers.ModelSerializer):
            class Meta:
                model = Company
                fields = ['id','name','typ','service_typ','code']

        roles = UserManagementtDetailsOutputRoles()
        company = UserManagementDetailsOutputCompany()
        
        class Meta:
            model = User
            fields = ['id','username','first_name_fa','last_name_fa','address',
                      'accessible_shrh_layers',
                      'accessible_contracts',
                      'accessible_initialborders',
                      'first_name','last_name','email','is_staff','is_controller',
                      'phonenumber','codemeli','fax','start_access','end_access',
                      'date_joined','last_login','is_active','roles','company']
                      
    class UserManagementDetailsInputSerializer(serializers.ModelSerializer):
        accessible_shrh_layers = serializers.ListField(
            child=serializers.IntegerField(),
            required=False,
            allow_empty=True,
        )
        accessible_contracts = serializers.ListField(
            child=serializers.UUIDField(),
            required=False,
            allow_empty=True,
        )
        accessible_initialborders = serializers.ListField(
            child=serializers.IntegerField(),
            required=False,
            allow_empty=True,
        )

        def validate_accessible_shrh_layers(self, value):
            """
            Validate that all provided ShrhLayer IDs exist
            """
            if value:
                existing_ids = ShrhLayer.objects.filter(id__in=value).values_list('id', flat=True)
                invalid_ids = set(value) - set(existing_ids)
                if invalid_ids:
                    raise serializers.ValidationError(
                        f"لایه‌های با شناسه‌های {list(invalid_ids)} یافت نشدند"
                    )
            return value
        def validate_accessible_contracts(self, value):
            if value:
                existing = Contract.objects.filter(id__in=value).values_list("id", flat=True)
                invalid = set(value) - set(existing)
                if invalid:
                    raise serializers.ValidationError(
                        f"قراردادهای با شناسه‌های {list(invalid)} یافت نشدند"
                    )
            return value

        def validate_accessible_initialborders(self, value):
            if value:
                existing = InitialBorder.objects.filter(id__in=value).values_list("id", flat=True)
                invalid = set(value) - set(existing)
                if invalid:
                    raise serializers.ValidationError(
                        f"مرزهای اولیه با شناسه‌های {list(invalid)} یافت نشدند"
                    )
            return value

        def update(self, instance, validated_data):
            """
            Update user instance with accessible_shrh_layers
            """
            shrh_layers = validated_data.pop('accessible_shrh_layers', None)
            contracts = validated_data.pop('accessible_contracts', None)
            init_borders = validated_data.pop('accessible_initialborders', None)
            
            # Update regular fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            
            instance.save()
            
            # --- Use user's existing access-control functions ---

            # ShrhLayers
            if shrh_layers is not None:
                instance.revoke_all_sharhlayer_access()
                layers = ShrhLayer.objects.filter(id__in=shrh_layers)
                instance.grant_bulk_sharhlayer_access(list(layers))

            # Contracts
            if contracts is not None:
                instance.revoke_all_contract_access()
                items = Contract.objects.filter(id__in=contracts)
                instance.grant_bulk_contract_access(list(items))

            # InitialBorders
            if init_borders is not None:
                instance.revoke_all_initialborder_access()
                items = InitialBorder.objects.filter(id__in=init_borders)
                instance.grant_bulk_initialborder_access(list(items))

            return instance
        class Meta:
            model = User
            fields = ['username','first_name_fa','last_name_fa','address',
                      'accessible_shrh_layers',
                      'accessible_contracts',
                      'accessible_initialborders',
                      'phonenumber','codemeli','fax','start_access','end_access',
                      'is_controller','first_name','last_name','email','roles','company']                  

    def get(self , request: Request , userid:int) -> Response:
        try:
            user_instance = User.objects.get(pk = userid)
            serializer = self.UserManagementtDetailsOutputSerializer(user_instance)

            user_activity_logger.info(f"دریافت اطلاعات کاربر {user_instance.username}" , extra=get_details_from_request(request))
            return Response(serializer.data , status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"detail": "کاربر با این آیدی پیدا نشد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:                      
            user_activity_logger.error(f"خطا در دریافت اطلاعات کاربر {str(e)}" , extra=get_details_from_request(request))
            return Response(
                {"detail": "خطا در خواندن کاربر"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def put(self , request: Request , userid:int) -> Response:
        try:
            user_instance = User.objects.get(pk=userid)
            
            # Serialize the incoming data
            serializer = self.UserManagementDetailsInputSerializer(
                user_instance, 
                data=request.data, 
                partial=True  # Allow partial updates
            )
            
            if not serializer.is_valid():
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

            # Update the user
            updated_user = serializer.save()
            # updated_user.sync_accessible_contracts()
            
            output_serializer = self.UserManagementtDetailsOutputSerializer(updated_user)

            user_activity_logger.info(f"ویرایش اطلاعات کاربر {updated_user.username}" , extra=get_details_from_request(request))

            return Response(output_serializer.data,status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {"detail": "کاربر با این آیدی پیدا نشد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:                      
            user_activity_logger.error(f"خطا در ویرایش اطلاعات کاربر {str(e)}" , extra=get_details_from_request(request))
            return Response(
                {"detail": "خطا در ویرایش کاربر"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self , request: Request , userid:int) -> Response:
        try:
            user_instance = User.objects.get(pk = userid)
            user_instance.delete()
            delete_logger.warning(f"حذف کاربر {user_instance.username}" , extra=get_details_from_request(request))

            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(
                {"detail": "کاربر با این آیدی پیدا نشد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:                      
            user_activity_logger.error(f"خطا در خذف کاربر {str(e)}" , extra=get_details_from_request(request))

            return Response(
                {"detail": "خطا در حذف کاربر"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )