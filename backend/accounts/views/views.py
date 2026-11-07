import logging
from datetime import datetime, timedelta, UTC
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from typing import Tuple
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import exceptions , status
from rest_framework.response import Response
from rest_framework.request import Request
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password as django_validate_password
from accounts.tokenization import create_access_token , create_refresh_token ,decode_refresh_token
from rest_framework.permissions import (
    IsAuthenticated
)
from django.conf import settings
from django.db.models import Q , Prefetch

from accounts.models import (
    User,
    Apis,
    Tools,
    Roles,
    Notification,
)
from initialborders.models.models import (
    InitialBorder,
    InitialBorderDomin,
)
from contracts.models.models import (
    Contract,
    ContractDomin,
)
from common.utils.ipget import get_client_ip
from common.models import Province , Company
from common.pagination import CustomPagination
from common.services.notification_services import NotificationFactory 
from common.mixins import SearchMixin
from accounts.services.auth import (
    verify_captcha , 
    complete_login , 
    authenticate_with_password,
    set_refresh_cookie
)
from accounts.exceptions import LoginError,InvalidCaptcha
from logs.utils import get_details_from_request

user_activity_logger = logging.getLogger('user_activity_logger')


class LoginUser(APIView):
    """
    API view for user authentication and token generation.
    """
    permission_classes = []
    authentication_classes = []

    class LoginInputSerializer(serializers.Serializer):
        username = serializers.CharField(
            max_length=150,
            help_text="نام کاربری",
            required=True,
            error_messages={
                'required': 'نام کاربری الزامی است',
                'blank': 'نام کاربری نمی‌تواند خالی باشد',
                'max_length': 'نام کاربری نمی‌تواند بیشتر از ۱۵۰ کاراکتر باشد'
            }
        )
        password = serializers.CharField(
            max_length=128,
            help_text="رمز عبور",
            required=True,
            style={'input_type': 'password'},
            error_messages={
                'required': 'رمز عبور الزامی است',
                'blank': 'رمز عبور نمی‌تواند خالی باشد',
                'max_length': 'رمز عبور نمی‌تواند بیشتر از ۱۲۸ کاراکتر باشد'
            }
        )
        rememberMe = serializers.BooleanField(
            default=False,
            required=False,
            help_text="مرا به خاطر بسپار"
        )
        captcha_id = serializers.CharField(
            max_length=150,
            help_text="نام کاربری",
            required=True,
            error_messages={
                'required': 'شناسه کپچا الزامی است',
                'blank': 'شناسه کپچا نمی‌تواند خالی باشد',
                'max_length': 'شناسه کپچا نمی‌تواند بیشتر از ۱۵۰ کاراکتر باشد'
            }
        )
        captcha_answer = serializers.CharField(
            max_length=150,
            help_text="نام کاربری",
            required=True,
            error_messages={
                'required': 'شناسه کپچا الزامی است',
                'blank': 'شناسه کپچا نمی‌تواند خالی باشد',
                'max_length': 'پاسخ کپچا نمی‌تواند بیشتر از ۱۵۰ کاراکتر باشد'
            }
        )
    class LoginOutputSerializer(serializers.Serializer):
        token = serializers.CharField()
        user = serializers.DictField(
            help_text="اطلاعات کاربر",
            child=serializers.CharField(),
            allow_empty=False
        )

    def post(self, request):
        data = self.LoginInputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        v = data.validated_data

        client_ip = get_client_ip(request=request)
        extra = get_details_from_request(request)
        user_activity_logger.info(f"تلاش برای ورود با نام کاربری {v['username']}", extra=extra)

        try:
            if not settings.DEBUG:
                verify_captcha(v["captcha_id"], v["captcha_answer"])

            user = authenticate_with_password(v["username"], v["password"], client_ip)
            result = complete_login(user, client_ip)
        except (LoginError, InvalidCaptcha) as e:
            user_activity_logger.warning(
                f"ورود ناموفق ({e.get_codes()}) برای {v['username']}", extra=extra)
            raise  # DRF returns {"detail": ...} with the exception's status code

        response = Response(self.LoginOutputSerializer({
            "token": result.access_token,
            "user": {"id": str(user.id), "username": user.username},
        }).data)
        set_refresh_cookie(response, result.refresh_token, v["rememberMe"])

        user_activity_logger.info(f"ورود موفق برای کاربر {user.username}", extra=extra)
        return response


class RefreshToken(APIView):
    permission_classes = []
    authentication_classes = []

    class RefreshTokenResponseSerializer(serializers.Serializer):
        token = serializers.CharField(help_text="New access token")
  
    def post(self, request:Request)->Response:
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            user_id = decode_refresh_token(refresh_token)
            new_access_token = create_access_token(user_id=user_id, expires_in_seconds=9000)

            return Response({
                'token': new_access_token    
            })

        except Exception as e:
            return Response(
                {'detail': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class LogoutUser(APIView): 
  permission_classes = [IsAuthenticated]

  class LogoutResponseSerializer(serializers.Serializer):
        detail = serializers.CharField(help_text="پیام تایید خروج")
  
  def post(self, request:Request) -> Response:

    #TODO: add access token to blocklist token lists in redis or in database and check it in auth
    response = Response()
    response_data = self.LogoutResponseSerializer({
        'detail': 'خروج با موفقیت انجام شد'
    })
    response.delete_cookie(key='refresh_token')    
    response.data = response_data.data
    response.status_code = status.HTTP_200_OK

    user_activity_logger.info(f"خروج موفق کاربر" , extra=get_details_from_request(request))

    return response
  
class UserProfile(APIView):
    permission_classes = [IsAuthenticated]
    """
    Authenticated user get and update their own profile
    GET: Retrieve user profile data
    PUT: Update user profile data
    """
    class UserProfileInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                "first_name","last_name",
                "first_name_fa","last_name_fa",
                "address","email",
                'phonenumber','codemeli','fax',
            ]

    class UserProfileOutputSerializer(serializers.ModelSerializer):
        class UserProfileOutputSerializerRoles(serializers.ModelSerializer):
            class UserProfileOutputSerializerRolesApis(serializers.ModelSerializer):
                class Meta:
                    model = Apis
                    fields = ['id' , 'method' , 'url' , 'desc']
            class UserProfileOutputSerializerRolesTools(serializers.ModelSerializer):
                class Meta:
                    model = Tools
                    fields = ['id' , 'title' , 'desc']
            apis = UserProfileOutputSerializerRolesApis(many=True)
            tools = UserProfileOutputSerializerRolesTools(many=True)
            class Meta:
                model = Roles
                fields = ['id' , 'apis' , 'tools' , 'title' , 'desc']

        class UserProfileOutputSerializerCompany(serializers.ModelSerializer):
            class Meta:
                model = Company
                fields = ['id','name','typ','service_typ','code']
        roles = UserProfileOutputSerializerRoles()
        company = UserProfileOutputSerializerCompany()
        class Meta:
            model = User
            fields = [
                "username","first_name","last_name",
                "first_name_fa","last_name_fa",
                'phonenumber','codemeli','fax','start_access','end_access',
                "address","email","last_login",'is_controller',
                "is_staff","is_superuser","roles","company",
            ]

    def get(self , request:Request) -> Response:
        try:
            user : User = request.user
            if not user or not user.is_authenticated:
                user_activity_logger.error(f"دریافت ناموفق اطلاعات کاربری {user.username}" , extra=get_details_from_request(request))
                raise Exception("کاربر نامعتبر است")
            
            serialized_data = self.UserProfileOutputSerializer(user)

            user_activity_logger.error(f"دریافت موفق اطلاعات کاربری {user.username}" , extra=get_details_from_request(request))

            return Response(serialized_data.data,status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"detail":"کاربر یافت نشد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            user_activity_logger.error(f"خطا در دریافت مشخصات کاربر {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail":"خطا در دریافت مشخصات کاربر"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def put(self, request:Request) -> Response:
        try:
            with transaction.atomic():
                user : User = request.user
                if not user or not user.is_authenticated:
                    raise Exception("کاربر نامعتبر است")
                
                serializer = self.UserProfileInputSerializer(user, data=request.data, context={'request': request}, partial=True)
                
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                serializer.save()

                updated_data = self.UserProfileOutputSerializer(user)
                user_activity_logger.warning(f"بروزرسانی موفق اطلاعات کاربری {user.username}", extra=get_details_from_request(request))
                return Response(updated_data.data, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({"detail":"کاربر یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            user_activity_logger.error(f"خطا در بروزرسانی مشخصات کاربر {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail":"خطا در بروزرسانی مشخصات کاربر"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Register(APIView):
    """
    Register new users with validation data
    Uses CustomPasswordValidator from validators.py for validate the password

    After a successful registration, the user is Automatically logged in.
    """
    permission_classes = []
    authentication_classes = []

    class RegisterOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                "username","first_name","last_name",
                "first_name_fa","last_name_fa",
                "address","email","last_login",
                "is_staff","is_superuser",
            ]

    class RegisterInputSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True, required=True)
        confirm_password = serializers.CharField(write_only=True, required=True)
        
        class Meta:
            model = User
            fields = [
                "username", "email", "password", "confirm_password",
                "first_name", "last_name", "first_name_fa", "last_name_fa", 
                "address"
            ]
        
        def validate(self, data):
            # Check if passwords match
            if data.get('password') != data.get('confirm_password'):
                raise serializers.ValidationError({"confirm_password": "رمز عبور و تکرار آن مطابقت ندارند"})
            
            # Apply custom password validation
            try:
                # Import auth password validators from settings
                from django.contrib.auth.password_validation import validate_password
                # This will use your CustomPasswordValidator from settings.AUTH_PASSWORD_VALIDATORS
                validate_password(data.get('password'))
            except Exception as e:
                raise serializers.ValidationError({"password": e.messages})
                
            return data


    def post(self, request:Request) -> Response:
        try:
            with transaction.atomic():
                serializer = self.RegisterInputSerializer(data=request.data)

                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                validated_data = serializer.validated_data

                # Remove confirm_password from data before creating user
                validated_data.pop('confirm_password')

                # Create user with validated data
                password = validated_data.pop('password')
                user = User.objects.create(**validated_data)
                user.set_password(password)  # Set password securely (hashed)
                user.save()

                access_token = create_access_token(user_id=user.id, expires_in_seconds=9000)
                
                response = Response({
                    "token": access_token,
                    "detail": self.RegisterOutputSerializer(user).data
                }, status=status.HTTP_201_CREATED)
                
                refresh_token = create_refresh_token(user_id=user.id, expires_in_days=7)
                self._set_refresh_token_cookie(response=response, refresh_token=refresh_token, max_age=None)

                file_logger.info(f"ثبت نام موفق کاربر {user.username}" , extra=get_details_from_request(request))

                return response
        
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ثبت نام کاربر"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def _set_refresh_token_cookie(self, response: Response, refresh_token: str, max_age: int = None) -> None:
        """
        Set the refresh token cookie.
        """        
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,  # Not accessible via JavaScript
            max_age=max_age,
        )

class UserContracts(SearchMixin, APIView):
    """
    GET: initial borders the user can access, each with the contract it belongs to
         (the contract is only included if the user also has access to it).

         - superuser: all initial borders / all contracts
         - others: User.get_accessible_initialborder() / User.get_accessible_contracts()
    """
    permission_classes = [IsAuthenticated]

    class UserInitialBorderListOutputSerializer(serializers.ModelSerializer):
        class UserInitialBorderProvinceSerializer(serializers.ModelSerializer):
            class Meta:
                model = Province
                fields = ['id', 'name_fa']

        class UserInitialBorderDtypSerializer(serializers.ModelSerializer):
            class Meta:
                model = InitialBorderDomin
                fields = ['id', 'title', 'code']

        class UserContractSerializer(serializers.ModelSerializer):
            class UserContractDtypSerializer(serializers.ModelSerializer):
                class Meta:
                    model = ContractDomin
                    fields = ['id', 'title', 'code']

            dtyp = UserContractDtypSerializer()

            class Meta:
                model = Contract
                fields = ['id', 'title', 'dtyp', 'number']

        province = UserInitialBorderProvinceSerializer(many=True)
        dtyp = UserInitialBorderDtypSerializer()
        # set in the view: the contract, or None if unattached / user has no access
        contract = UserContractSerializer(source='accessible_contract', read_only=True, allow_null=True)

        class Meta:
            model = InitialBorder
            fields = ['id', 'title', 'dtyp', 'parentid', 'province', 'center', 'bbox', 'contract']

    def get(self, request: Request) -> Response:
        try:
            user: User = request.user

            # 1. base querysets by role
            if user.is_superuser:
                initial_borders = InitialBorder.objects.all()
                accessible_contract_ids = set(Contract.objects.values_list('id', flat=True))
            else:
                initial_borders = user.get_accessible_initialborder()
                accessible_contract_ids = set(
                    user.get_accessible_contracts().values_list('id', flat=True)
                )

            initial_borders = (
                initial_borders
                .select_related('dtyp', 'contract__dtyp')
                .prefetch_related('province')
            )

            # 2. search (contract title/number only match contracts the user can access)
            search = request.query_params.get('search', '').strip()
            if search:
                initial_borders = initial_borders.filter(
                    Q(title__icontains=search)
                    | (
                        Q(contract_id__in=accessible_contract_ids)
                        & (Q(contract__title__icontains=search) | Q(contract__number__icontains=search))
                    )
                )

            # 3. paginate at the DB level, then attach the accessible contract
            paginator = CustomPagination()
            page = paginator.paginate_queryset(initial_borders.order_by('-id'), request)
            for border in page:
                border.accessible_contract = (
                    border.contract if border.contract_id in accessible_contract_ids else None
                )

            serializer = self.UserInitialBorderListOutputSerializer(
                page, many=True, context={'request': request}
            )

            user_activity_logger.info(
                f"دریافت موفق محدوده‌های اولیه کاربر {user.username}",
                extra=get_details_from_request(request),
            )
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            user_activity_logger.error(
                f"خطا در خواندن محدوده‌های اولیه مربوط به کاربر {str(e)}",
                extra=get_details_from_request(request),
            )
            return Response(
                {"detail": "خطا در خواندن محدوده‌های اولیه مربوط به کاربر"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
class NotificationListApiViews(APIView):
    """
        Send a List of Notifications for user
    """
    permission_classes = [IsAuthenticated]

    class NotificationListOutputSerializer(serializers.ModelSerializer):
        class NotificationListOutputSerializerUser(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ['id','username']

        sender = NotificationListOutputSerializerUser()

        class Meta:
            model = Notification
            fields = ['id','sender','subject','is_read','created_at']

    def get(self, request:Request) -> Response:
        try:
            user = request.user
            
            # Get week parameter from query params, default to 1
            week_param = request.query_params.get('week', '1')
            
            # Try to convert to int, default to 1 if invalid
            try:
                weeks_ago = int(week_param)
                # Ensure positive number
                if weeks_ago < 1:
                    weeks_ago = 1
            except (ValueError, TypeError):
                weeks_ago = 1
            
            end_date = timezone.now()
            start_date = end_date - timedelta(weeks=weeks_ago)
            
            # Filter notifications for the specified week range
            all_related_notif_to_user = Notification.objects.filter(
                receiver=user,
                created_at__gte=start_date,
                created_at__lte=end_date
            )
            
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(all_related_notif_to_user, request)
            serializer = self.NotificationListOutputSerializer(paginated_queryset, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن اعلان‌های مربوط به کاربر"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NotificationDetailsApiViews(APIView):
    """
        GET: Retrive a Notification with detail fields
        Delete: Delete A Notification Instance
    """
    permission_classes = [IsAuthenticated]

    class NotificationDetailsOutputSerializer(serializers.ModelSerializer):
        class NotificationDetailsOutputSerializerUser(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ['id','username','first_name','last_name','email']

        sender = NotificationDetailsOutputSerializerUser()

        class Meta:
            model = Notification
            fields = ['id','sender','subject','is_read','text','created_at']

    def get(self, request:Request, notifid:int) -> Response:
        try:
            thisuser = request.user
            notif_instance = Notification.objects.get(pk=notifid)     
            if notif_instance.receiver != thisuser:
                raise Exception("user not allow to see this notif")
            serialzied_notif = self.NotificationDetailsOutputSerializer(notif_instance)
            notif_instance.is_read = True
            notif_instance.save()
            return Response(serialzied_notif.data , status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"detail": "اعلان مورد نظر یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن اعلان‌"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request:Request, notifid:int) -> Response:
        try:
            user = request.user
            notif_instance = Notification.objects.get(pk=notifid)     
            if notif_instance.receiver != request.user:
                raise Exception("user not allow to see this notif")
            notif_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Notification.DoesNotExist:
            return Response({"detail": "اعلان مورد نظر یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در حذف اعلان‌"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ChangePassword(APIView):
    """
        Change password by user itself
    """
    permission_classes = [IsAuthenticated]

    class ChangePasswordInputSerializer(serializers.Serializer):
        current_password = serializers.CharField(
            write_only=True,
            required=True,
            style={'input_type': 'password'},
            error_messages={
                'required': 'رمز عبور فعلی الزامی است',
                'blank': 'رمز عبور فعلی نمی‌تواند خالی باشد',
            }
        )
        new_password = serializers.CharField(
            write_only=True,
            min_length=8,
            required=True,
            style={'input_type': 'password'},
            error_messages={
                'required': 'رمز عبور جدید الزامی است',
                'min_length': 'رمز عبور جدید باید حداقل ۸ کاراکتر باشد',
                'blank': 'رمز عبور جدید نمی‌تواند خالی باشد',
            }
        )
        confirm_new_password = serializers.CharField(
            write_only=True,
            required=True,
            style={'input_type': 'password'},
            error_messages={
                'required': 'تکرار رمز عبور جدید الزامی است',
                'blank': 'تکرار رمز عبور جدید نمی‌تواند خالی باشد',
            }
        )

        def validate_new_password(self, password):
            """
            Validate password using Django's password validators from settings
            """
            try:
                django_validate_password(password)
            except ValidationError as e:
                raise serializers.ValidationError(e.messages)
            return password

        def validate(self, attrs):
            new_password = attrs.get('new_password')
            confirm_new_password = attrs.get('confirm_new_password')

            if new_password != confirm_new_password:
                raise serializers.ValidationError({
                    'confirm_new_password': 'رمز عبور جدید و تکرار آن باید یکسان باشند'
                })

            return attrs

    def put(self , request:Request) -> Response: 
        try:
            user : User = request.user
            if not user or not user.is_authenticated:
                user_activity_logger.error(f"دریافت ناموفق اطلاعات کاربری" , extra=get_details_from_request(request))
                raise Exception("کاربر نامعتبر است")

            serializer = self.ChangePasswordInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            validated_data = serializer.validated_data
            current_password = validated_data['current_password']
            new_password = validated_data['new_password']

            if not user.check_password(current_password):
                user_activity_logger.warning(f"تلاش ناموفق تغییر گذرواژه با رمز فعلی نادرست برای کاربر {user.username}", extra=get_details_from_request(request))
                return Response({"detail": "رمز عبور فعلی صحیح نیست"}, status=status.HTTP_400_BAD_REQUEST)

            if current_password == new_password:
                return Response({"detail": "رمز عبور جدید نمی‌تواند با رمز عبور فعلی یکسان باشد"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save(update_fields=['password'])

            user_activity_logger.warning(f"گذرواژه کاربر {user.username} با موفقیت تغییر کرد", extra=get_details_from_request(request))
            
            return Response({"detail":"گذرواژه شما با موفقیت تغییر کرد"},status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"detail":"کاربر یافت نشد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            user_activity_logger.error(f"خطا در تغییر گذرواژه کاربر {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail":"خطا در تغییر گذرواژه کاربر"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
