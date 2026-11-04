import os
import shutil
import logging
import zipfile
import uuid
from datetime import datetime
from django.db import transaction
from logs.utils import get_details_from_request
from rest_framework.response import Response
from rest_framework.request import Request
from django.db.models import Model as DjangoModel
from rest_framework import serializers
from django.http import FileResponse
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.validators import FileExtensionValidator
from common.pagination import CustomPagination
from django.conf import settings
from layers.exceptions import GeoDatabaseValidationError

from layers.utils import get_model_from_string
from layers.apps import LayersConfig

from common.services.notification_services import NotificationFactory
from common.services.gis import queryset_to_shapefile

from accounts.models import User

from contracts.models.models import (
    ContractDomin,
    Contract,
    ContractBorder,
    ShrhBase,
    ShrhLayer
)
from layers.models.models import (
    LayersNames,
    LinkedToLayerTable,
)
from layers.services.gis import (
    process_layer_data,
    get_shape_columns_from_zipfile,
    convert_tif_to_cog_and_save_to_rasterdir,)

from accounts.permissions import (
    HasDynamicPermission,
    HasShrhLayerAccess,
)

delete_logger = logging.getLogger('delete_activity_logger')


class LayerNamesListApiView(APIView):
    """
        get ContractDomain.CODE as url input
        return all layernames filtered by ContractDomain.CODE
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    class LayerNamesListOutputSerializer(serializers.ModelSerializer):

        class Meta:
            model = LayersNames
            fields = ['id','lyrgroup_en','lyrgroup_fa','layername_en','layername_fa','geometrytype']


    def get(self , request:Request , contractcode:int):
        try:
            contractdomain_instance = ContractDomin.objects.get(code=contractcode)
            all_layernames = LayersNames.objects.filter(dtyp=contractdomain_instance)
            serializer = self.LayerNamesListOutputSerializer(all_layernames,many=True)
            # Group the data base in lyrgroup_fa
            grouped_data = {}
            for item in serializer.data:
                group_key = item['lyrgroup_fa'] or "بدون گروه"
                grouped_data.setdefault(group_key, []).append(item)
            return Response(grouped_data, status=status.HTTP_200_OK)
        except ContractDomin.DoesNotExist:
            return Response({"detail":"نوع قراردادی با این کد پیدا نشد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن نام لایه ها"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AllLayersOfAContractListApiView(APIView):
    """
    API endpoint to list all ShrhLayers of a contract with filtering and grouping options.
    
    This endpoint is designed for User (Not Admin)
    
    Query Parameters:
        - groupby: Group layers by 'layergroupen', 'layergroupfa', or 'shrhtitle' (default: 'layergroupen')
        - lyrstatus: Filter by upload status - 'all', 'onlyuploaded', or 'onlyempty' (default: 'all')
    
    Returns:
        Grouped dictionary of layers based on the groupby parameter
    """

    class AllLayersOfAContractListOutputSerializer(serializers.ModelSerializer):
        """Main serializer for ShrhLayer objects with nested related data"""
        
        class AllLayersOfAContractListOutputSerializerLayername(serializers.ModelSerializer):
            """Nested serializer for LayersNames model"""
            class Meta:
                model = LayersNames
                fields = ['dtyp', 'lyrgroup_en', 'lyrgroup_fa', 
                         'layername_en', 'layername_fa', 'geometrytype']
        
        class AllLayersOfAContractListOutputSerializerUser(serializers.ModelSerializer):
            """Nested serializer for User model (verifier)"""
            class Meta:
                model = User
                fields = ['id', 'username', 'first_name_fa', 'last_name_fa']
        
        class AllLayersOfAContractListOutputSerializerShrhBase(serializers.ModelSerializer):
            """Nested serializer for ShrhBase model"""
            class Meta:
                model = ShrhBase
                fields = ['id', 'title','faz']
        
        # Nested serializer fields
        layer_name = AllLayersOfAContractListOutputSerializerLayername()
        verified_by = AllLayersOfAContractListOutputSerializerUser()
        last_uploaded_by = AllLayersOfAContractListOutputSerializerUser()
        shrh_base = AllLayersOfAContractListOutputSerializerShrhBase()

        class Meta:
            model = ShrhLayer
            fields = ['id', 'shrh_base', 'layer_name', 'raster_uuid', 'scale', 'is_uploaded', 'status',
                     'last_uploaded_date','last_uploaded_by', 'upload_count', 'is_verified', 'verified_by', 'verified_at']

    # Valid choices for query parameters
    GROUPBY_CHOICES = ['layergroupen', 'layergroupfa', 'shrhtitle']
    LYRSTATUS_CHOICES = ['all', 'onlyuploaded', 'onlyempty']

    def _validate_query_params(self, request: Request) -> tuple[str|None, str|None, Response|None]:
        """
        Validate and return query parameters.
        
        Returns:
            tuple: (groupby, lyrstatus, error_response)
            If validation fails, error_response will be a Response object, otherwise None
        """
        # Validate groupby parameter
        groupby = request.query_params.get('groupby', 'layergroupen')
        if groupby not in self.GROUPBY_CHOICES:
            return None, None, Response(
                {"detail": f"گروه‌بندی میتواند فقط {', '.join(self.GROUPBY_CHOICES)} باشد"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate lyrstatus parameter
        lyrstatus = request.query_params.get('lyrstatus', 'all')
        if lyrstatus not in self.LYRSTATUS_CHOICES:
            return None, None, Response(
                {"detail": f"وضعیت بارگذاری لایه میتواند فقط {', '.join(self.LYRSTATUS_CHOICES)} باشد"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return groupby, lyrstatus, None

    def _get_filtered_layers(
            self,
            contract_instance: Contract,
            contract_border_instance:ContractBorder,
            user_instance:User,
            lyrstatus: str | None
        ):
        """
        Get ShrhLayer queryset filtered by upload status.
        
        Args:
            contract_instance: Contract object
            contract_instance: Contract object
            user_instance: User object
            lyrstatus: Filter status ('all', 'onlyuploaded', 'onlyempty')
            
        Returns:
            QuerySet: Filtered ShrhLayer objects
        """
        base_queryset = ShrhLayer.objects.filter(
            shrh_base__contract=contract_instance,
            contractborder=contract_border_instance
        ).select_related(
            'shrh_base', 
            'layer_name', 
            'verified_by'
        ).order_by('shrh_base__title', 'layer_name__layername_en')

        # Apply user access restriction (skip for superuser)
        if not user_instance.is_superuser:
            base_queryset = base_queryset.filter(
                accessible_by_users=user_instance
            )

        
        # Apply status filter
        if lyrstatus is None: # 'all'
            return base_queryset
        elif lyrstatus == 'onlyuploaded':
            return base_queryset.filter(is_uploaded=True)
        elif lyrstatus == 'onlyempty':
            return base_queryset.filter(is_uploaded=False)
        else:  # 'all'
            return base_queryset

    def _get_group_key_function(self, groupby: str):
        """
        Get the appropriate grouping function based on groupby parameter.
        
        Args:
            groupby: Grouping parameter ('layergroupen', 'layergroupfa', 'shrhtitle')
            
        Returns:
            function: Lambda function to extract group key from serialized item
        """
        group_key_functions = {
            'layergroupen': lambda item: item['layer_name']['lyrgroup_en'] or "no group",
            'layergroupfa': lambda item: item['layer_name']['lyrgroup_fa'] or "بدون گروه",
            'shrhtitle': lambda item: item['shrh_base']['title'] or "بدون عنوان"
        }
        return group_key_functions[groupby]

    def _group_serialized_data(self, serialized_data, groupby: str) -> dict:
        """
        Group serialized data based on the specified groupby parameter.
        
        Args:
            serialized_data: Serialized layer data
            groupby: Grouping parameter
            
        Returns:
            dict: Grouped data with group names as keys and lists of items as values
        """
        group_key_getter = self._get_group_key_function(groupby)
        grouped_data = {}
        
        for item in serialized_data.data:
            group_key = group_key_getter(item)
            grouped_data.setdefault(group_key, []).append(item)
        
        return grouped_data

    def get(self, request: Request, contractid: str, contractborderid: str) -> Response:
        """
        Get all layers of a contract with optional filtering and grouping.
        
        Args:
            request: HTTP request object
            contractid: UUID of the contract
            contract border id: UUID of the contractborder
        Returns:
            Response: Grouped layers data or error response
        """
        try:
            user = request.user

            # Verify contract exists
            contract_instance = Contract.objects.get(pk=contractid)
            contract_border_instance = ContractBorder.objects.get(pk=contractborderid)

            if contract_instance !=contract_border_instance.contract:
                return Response({"detail":"این محدوده قرارداد به این قرارداد مربوط نیست!"},status=status.HTTP_400_BAD_REQUEST)
            
            # Validate query parameters
            groupby, lyrstatus, error_response = self._validate_query_params(request)
            if error_response:
                return error_response
            
            # Get filtered layers
            shrh_layers = self._get_filtered_layers(contract_instance, contract_border_instance, user , lyrstatus)
            
            # Serialize the data
            serialized_data = self.AllLayersOfAContractListOutputSerializer(shrh_layers, many=True)
            
            # Group the serialized data
            grouped_data = self._group_serialized_data(serialized_data, groupby)
            
            return Response(grouped_data, status=status.HTTP_200_OK)
            
        except Contract.DoesNotExist:
            return Response(
                {"detail": "قراردادی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except ContractBorder.DoesNotExist:
            return Response(
                {"detail": "محدوده قراردادی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error in AllLayersOfAContractListApiView: {e}")
            return Response(
                {"detail": "خطا در خواندن لایه‌های شرح خدمات"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class UploadVectorLayerApiView(APIView):
    """
    Upload New Layer
    - Get the user from request
    - Get sharkhadamatLayer from body of request
    - Check user access to this sharkhadamatLayer
    - Check  is_verified be False
    - Get the layer model from sharhkhadamatLayer.layer_name.layername_en
    - Update is_uploaded last_uploaded_date upload_count
    """

    permission_classes = [HasDynamicPermission , HasShrhLayerAccess]

    class VectorLayerInputSerializer(serializers.Serializer):
        shrhlyr_id = serializers.IntegerField(
            required=True,
            allow_null=False
        )
        file = serializers.FileField(
            required=True,
            allow_null=False,
            validators=[
                FileExtensionValidator(
                    allowed_extensions=['zip'],
                    message="فایل محدوده حتما باید با فرمت zip باشد"
                )
            ]
        )
        matched_fields = serializers.JSONField(
            required=True,
            allow_null=False
        )
        attach_to_existing = serializers.BooleanField(
            required=False,
            default=False,
            help_text=(
                "true: داده‌های جدید به داده‌های موجود اضافه می‌شوند (attach). "
                "false: داده‌های قبلی حذف و با داده‌های جدید جایگزین می‌شوند (replace)."
            )
        )

        def validate_shrhlyr_id(self, value):
            if value <= 0:
                raise serializers.ValidationError("شناسه لایه باید عددی بزرگ‌تر از صفر باشد.")
            return value
        def validate_file(self, value):
            # Check file size
            max_size = 100 * 1024 * 1024  # 100 MB
            if value.size > max_size:
                raise serializers.ValidationError("File size cannot exceed 100 MB.")
            return value
        

    def post(self , request:Request) -> Response:
        try:
            user = request.user
            serializer = self.VectorLayerInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data
            
            zipfile_obj = validated_data['file']
            shrhlyr_id = validated_data['shrhlyr_id']
            matched_fields = validated_data['matched_fields'] 
            print("matched_fields  " , matched_fields)

            shrh_layer_instance : ShrhLayer = ShrhLayer.objects.get(pk=shrhlyr_id)
            print("shrh_layer_instance>>>>>>>>>",shrh_layer_instance)

            # HasShrhLayerAccess do this 
            # if not user.is_superuser and not user.has_sharhlayer_access(shrh_layer_instance):
            #     return Response({"detail": "کاربر به این لایه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)

            if shrh_layer_instance.is_verified:
                return Response(
                {"detail": "این لایه شرح‌خدمات تایید نهایی شده است و اجازه بارگذاری مجدد آن را ندارید"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

            if shrh_layer_instance.layer_name.geometrytype == "raster":
                return Response(
                    {"detail": "این api برای لایه های رستری قابل استفاده نیست"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            layer_model = get_model_from_string(model_app_label=LayersConfig.name ,
                                                model_class_name=shrh_layer_instance.layer_name.layername_en)
            print(">>>>>>>>>>>>>>>>" , layer_model)
            if layer_model is None:
                return Response(
                    {"detail": "جدول لایه مورد نظر یافت نشد"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            
            if not issubclass(layer_model, LinkedToLayerTable):
                raise Exception("layer model is not LinkedToLayerTable instance")
            
                        # if layer_model.objects.filter(shr_layer=shrh_layer_instance).exists():
            #     return Response(
            #         {"detail": "لایه مورد نظر از قبل موجود می‌باشد؛ در صورت تمایل، ابتدا آن را حذف و سپس بارگذاری مجدد نمایید."}, 
            #         status=status.HTTP_400_BAD_REQUEST
            #     )
            # just remember state, don't block or delete yet
            layer_already_exists = layer_model.objects.filter(shr_layer=shrh_layer_instance).exists()

            attach_to_existing = validated_data['attach_to_existing']

            
            result , data , message = process_layer_data(
                zipfile_obj = zipfile_obj,
                layer_model = layer_model,
                matched_fields = matched_fields,
                shrh_layer_instance = shrh_layer_instance,
            )

            if not result:
                return Response({"detail":message }, status=status.HTTP_400_BAD_REQUEST)

            #process layer data is successful
            instances = [layer_model(**item) for item in data]
            # layer_creation_result = layer_model.objects.bulk_create(instances)

            # shrh_layer_instance.mark_as_uploaded(user) #mark_as_uploaded is in model class 
            with transaction.atomic():
                if layer_already_exists and not attach_to_existing:
                    layer_model.objects.filter(shr_layer=shrh_layer_instance).delete()

                layer_creation_result = layer_model.objects.bulk_create(instances)
                shrh_layer_instance.mark_as_uploaded(user)

            #Send Notification
            NotificationFactory.for_layer_upload(uploader_user=request.user,sharhlayer=shrh_layer_instance)

            SMSFactory.send_layeradd_sms_to_mojries(uploader_user=request.user , shrhlayer=shrh_layer_instance)

            return Response({"message":f"لایه با {len(layer_creation_result)} عارضه با موفقیت ساخته شد"} , status=status.HTTP_201_CREATED)

        except ShrhLayer.DoesNotExist:
            return Response(
                {"detail": "لایه شرح خدماتی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        except Exception as e:
            print(f"Error in UploadVectorLayerApiView: {e}")
            return Response(
                {"detail": "خطا در بارگذاری لایه"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class ShpColumnOfVectorLayerApiView(APIView):
    """
        Get sharkhadamatLayer from body of request
        Check is zipeed shpefile is valid or not
        Return the columns of shape file in Response
    """
    class ShpColumnOfVectorLayerSerializer(serializers.Serializer):
        file = serializers.FileField(
            required=True,
            allow_null=False,
            validators=[
                FileExtensionValidator(
                    allowed_extensions=['zip'],
                    message="فایل محدوده حتما باید با فرمت zip باشد"
                )
            ]
        )
        def validate_file(self, value):
            # Check file size
            max_size = 100 * 1024 * 1024  # 100 MB
            if value.size > max_size:
                raise serializers.ValidationError("File size cannot exceed 100 MB.")
            return value
        
    def post(self , request:Request) -> Response:
        try:
            serializer = self.ShpColumnOfVectorLayerSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data
            
            zipfile_obj = validated_data['file']
            protected_columns = ['border','id','shr_layer','geom','geometry']

            result , shape_file_columns , message = get_shape_columns_from_zipfile(
                zipfile_obj = zipfile_obj
            )

            if not result:
                return Response({"detail":message }, status=status.HTTP_400_BAD_REQUEST)
            
            filterd_col_names = [col for col in shape_file_columns if col not in protected_columns]
            
            return Response(filterd_col_names , status=status.HTTP_200_OK)


        except Exception as e:
            print(f"Error in ShpColumnOfVectorLayerApiView: {e}")
            return Response(
                {"detail": "خطا در خواندن ستون های شیپ فایل"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class AllColumnOfSharhlayerApiView(APIView):
    """
        GET: return list of all sharh_layer table column name
        sharh_layer -> layername -> the table -> columns
    """
    
    permission_classes = [HasDynamicPermission , HasShrhLayerAccess]

    class AllColumnOfSharhlayerApiViewInputSerializer(serializers.Serializer):
        shrhlyr_id = serializers.IntegerField(
            required=True,
            allow_null=False
        )
        def validate_shrhlyr_id(self, value):
            if value <= 0:
                raise serializers.ValidationError("شناسه لایه باید عددی بزرگ‌تر از صفر باشد.")
            return value
        
    def post(self , request:Request) -> Response:
        try:
            serializer = self.AllColumnOfSharhlayerApiViewInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data
            
            shrhlyr_id = validated_data['shrhlyr_id']

            shrh_layer_instance : ShrhLayer = ShrhLayer.objects.get(pk=shrhlyr_id)
            
            # HasShrhLayerAccess do this 
            # if not user.is_superuser and not user.has_sharhlayer_access(shrh_layer_instance):
            #     return Response({"detail": "کاربر به این لایه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)

            if not shrh_layer_instance.layer_name:
                return Response(
                    {"detail": "این لایه به نام لایه ایی متصل نیست"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not shrh_layer_instance.layer_name.layername_en:
                return Response(
                    {"detail": "این لایه به نام لایه معتبری متصل نیست"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            if shrh_layer_instance.layer_name.geometrytype == "raster":
                return Response(
                    {"detail": "این api برای لایه های رستری قابل استفاده نیست"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            layer_model = get_model_from_string(model_app_label=LayersConfig.name ,
                                                model_class_name=shrh_layer_instance.layer_name.layername_en)
            
            if layer_model is None:
                return Response(
                    {"detail": "جدول لایه مورد نظر یافت نشد"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not issubclass(layer_model, LinkedToLayerTable):
                raise Exception("layer model is not LinkedToLayerTable instance")
            
            protected_columns = ['border','id','shr_layer','geom','geometry']
            allcolumns = [col.name for col in layer_model._meta.fields if col.name not in protected_columns]
            
            return Response(allcolumns , status=status.HTTP_200_OK)

        except ShrhLayer.DoesNotExist:
            return Response(
                {"detail": "لایه شرح خدماتی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        except Exception as e:
            print(f"Error in AllColumnOfSharhlayer: {e}")
            return Response(
                {"detail": "خطا در خواندن ستون های دیتابیس لایه"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class DeleteVectorLayerApiView(APIView):
    """
        - Get sharkhadamatLayer id from body of request
        - Get the layer model class from sharkhadamatLayer.layer_name.layername_en
        - Check sharkhadamatLayer.is_verified be FALSE
        - Check the model if have a record with this sharkhadamatLayer id
        - Delete it
        - make sharkhadamatLayer.is_uploaded false
    """
    permission_classes = [HasDynamicPermission , HasShrhLayerAccess]

    class DeleteVectorLayerInputSerializer(serializers.Serializer):
        shrhlyr_id = serializers.IntegerField(
            required=True,
            allow_null=False
        )
        def validate_shrhlyr_id(self, value):
            if value <= 0:
                raise serializers.ValidationError("شناسه لایه باید عددی بزرگ‌تر از صفر باشد.")
            return value
        
    def delete(self , request:Request) -> Response:
        try:
            serializer = self.DeleteVectorLayerInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data
            
            shrhlyr_id = validated_data['shrhlyr_id']

            shrh_layer_instance : ShrhLayer = ShrhLayer.objects.get(pk=shrhlyr_id)
            
            # HasShrhLayerAccess do this 
            # if not user.is_superuser and not user.has_sharhlayer_access(shrh_layer_instance):
            #     return Response({"detail": "کاربر به این لایه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)

            if shrh_layer_instance.is_verified:
                return Response(
                {"detail": "این لایه شرح‌خدمات تایید نهایی شده است و اجازه حذف آن را ندارید"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

            if shrh_layer_instance.layer_name.geometrytype == "raster":
                return Response(
                    {"detail": "این api برای لایه های رستری قابل استفاده نیست"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            layer_model = get_model_from_string(model_app_label=LayersConfig.name ,
                                                model_class_name=shrh_layer_instance.layer_name.layername_en)
            
            if layer_model is None:
                return Response(
                    {"detail": "جدول لایه مورد نظر یافت نشد"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            
            if not issubclass(layer_model, LinkedToLayerTable):
                raise Exception("layer model is not LinkedToLayerTable instance")
            
            layer_instances = layer_model.objects.filter(shr_layer=shrh_layer_instance)
            if not layer_instances.exists():
                return Response(
                    {"detail": "لایه مورد نظر برای حذف موجود نیست."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            layer_deleted_count, layer_deleted_objects_detail = layer_instances.delete()

            if layer_deleted_count <=0:
                return Response(
                    {"detail": "هیچ رکوردی حذف نشد."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            shrh_layer_instance.is_uploaded = False
            shrh_layer_instance.save()

            delete_logger.warning(f"حذف لایه ویکتوری از {shrh_layer_instance.id} با شرح خدمات لایه {shrh_layer_instance.layer_name.layername_fa} با {layer_deleted_count} عارضه  " , extra=get_details_from_request(request))

            return Response({"message":f"لایه با {layer_deleted_count} عارضه با موفقیت حدف شد"} , status=status.HTTP_200_OK)

        except ShrhLayer.DoesNotExist:
            return Response(
                {"detail": "لایه شرح خدماتی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        except Exception as e:
            print(f"Error in UploadVectorLayerApiView: {e}")
            return Response(
                {"detail": "خطا در حذف لایه"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RasterLayerApiView(APIView):
    """
    Upload New Layer
    - Get the user from request
    - Get the .tiif file from request
    - Get sharkhadamatLayer from body of request
    - Check user access to this sharkhadamatLayer
    - Check  is_verified be False
    - Get the layer model from sharhkhadamatLayer.layer_name.layername_en
    - Process the .tif file
    - Save it to /rasterdir/<uuid>/.tif file
    - Update is_uploaded last_uploaded_date upload_count
    """
    permission_classes = [HasDynamicPermission , HasShrhLayerAccess]

    class RasterLayerInputSerializer(serializers.Serializer):
        shrhlyr_id = serializers.IntegerField(
            required=True,
            allow_null=False
        )
        file = serializers.FileField(
            required=True,
            allow_null=False,
            # validators=[
            #     FileExtensionValidator(
            #         allowed_extensions=['.tif'],
            #         message="فایل رستری حتما باید با فرمت .tif باشد"
            #     )
            # ]
        )
        def validate_shrhlyr_id(self, value):
            if value <= 0:
                raise serializers.ValidationError("شناسه لایه باید عددی بزرگ‌تر از صفر باشد.")
            return value
        def validate_file(self, value):
            # Check file size
            max_size = 1000 * 1024 * 1024  # 1000 MB
            if value.size > max_size:
                raise serializers.ValidationError("Raster File size cannot exceed 1000 MB.")
            return value
        
    def post(self , request:Request) -> Response:
        try:
            user = request.user
            serializer = self.RasterLayerInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data
            
            tifffile_obj = validated_data['file']
            shrhlyr_id = validated_data['shrhlyr_id']

            shrh_layer_instance : ShrhLayer = ShrhLayer.objects.get(pk=shrhlyr_id)

            # HasShrhLayerAccess do this 
            # if not user.is_superuser and not user.has_sharhlayer_access(shrh_layer_instance):
            #     return Response({"detail": "کاربر به این لایه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)

            if shrh_layer_instance.is_verified:
                return Response(
                {"detail": "این لایه شرح‌خدمات تایید نهایی شده است و اجازه بارگذاری مجدد آن را ندارید"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

            if shrh_layer_instance.layer_name.geometrytype != "raster":
                return Response(
                    {"detail": "این api برای لایه های غیر رستری قابل استفاده نیست"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if shrh_layer_instance.raster_uuid and shrh_layer_instance.is_uploaded:
                return Response(
                    {"detail": "لایه مورد نظر از قبل موجود می‌باشد؛ در صورت تمایل، ابتدا آن را حذف و سپس بارگذاری مجدد نمایید."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
                
            
            result , raster_uuid , message = convert_tif_to_cog_and_save_to_rasterdir(
                tif_file = tifffile_obj,
            )

            if not result:
                return Response({"detail":message }, status=status.HTTP_400_BAD_REQUEST)
            
            shrh_layer_instance.raster_uuid = raster_uuid
            shrh_layer_instance.save()
            shrh_layer_instance.mark_as_uploaded(user) #mark_as_uploaded is in model class 

            #Send Notification
            NotificationFactory.for_layer_upload(uploader_user=request.user,sharhlayer=shrh_layer_instance)

            SMSFactory.send_layeradd_sms_to_mojries(uploader_user=request.user , shrhlayer=shrh_layer_instance)

            return Response({"message":f"{raster_uuid}"} , status=status.HTTP_201_CREATED)

        except ShrhLayer.DoesNotExist:
            return Response(
                {"detail": "لایه شرح خدماتی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        except Exception as e:
            print(f"Error in RasterLayerApiview: {e}")
            return Response(
                {"detail": "خطا در بارگذاری لایه رستری"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class DeleteRasterLayerApiView(APIView):
    """
    Delete A Raster LAyer
        - Get sharkhadamatLayer id from body of request
        - Check user Allow Permmisson to this sharkhadamatLayer
        - Check sharkhadamatLayer.is_verified be FALSE
        - Check sharkhadamatLayer.is_uploaded True & sharkhadamatLayer.raster_uuid have value
        - Delete the /Raster_root/harkhadamatLayer.raster_uuid/ directory
        - make sharkhadamatLayer.is_uploaded false & harkhadamatLayer.raster_uuid None
    """
    permission_classes = [HasDynamicPermission , HasShrhLayerAccess]

    class RasterLayerInputSerializer(serializers.Serializer):
        shrhlyr_id = serializers.IntegerField(
            required=True,
            allow_null=False
        )
        def validate_shrhlyr_id(self, value):
            if value <= 0:
                raise serializers.ValidationError("شناسه لایه باید عددی بزرگ‌تر از صفر باشد.")
            return value
        
    def delete(self , request:Request) -> Response:
        try:
            serializer = self.RasterLayerInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data
            
            shrhlyr_id = validated_data['shrhlyr_id']

            shrh_layer_instance : ShrhLayer = ShrhLayer.objects.get(pk=shrhlyr_id)

            # HasShrhLayerAccess do this 
            # if not user.is_superuser and not user.has_sharhlayer_access(shrh_layer_instance):
            #     return Response({"detail": "کاربر به این لایه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)

            if shrh_layer_instance.is_verified:
                return Response(
                {"detail": "این لایه شرح‌خدمات تایید نهایی شده است و اجازه خذف آن را ندارید"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

            if shrh_layer_instance.layer_name.geometrytype != "raster":
                return Response(
                    {"detail": "این api برای لایه های غیر رستری قابل استفاده نیست"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if shrh_layer_instance.raster_uuid is None and not shrh_layer_instance.is_uploaded:
                return Response(
                    {"detail": "لایه مورد نظر از موجود نمیباشد."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
                
            main_raster_dir = settings.RASTER_ROOT

            layer_raster_dir = os.path.join(main_raster_dir, str(shrh_layer_instance.raster_uuid))


            # Check if the directory exists before attempting to delete it
            if os.path.exists(layer_raster_dir):
                try:
                    shutil.rmtree(layer_raster_dir)
                    print(f"Directory '{layer_raster_dir}' has been successfully deleted.")
                    shrh_layer_instance.raster_uuid = None
                    shrh_layer_instance.is_uploaded = False
                    shrh_layer_instance.save()

                    delete_logger.warning(f"خدف لایه رستری از لایه {shrh_layer_instance.id} لایه {shrh_layer_instance.layer_name.layername_fa}" , extra=get_details_from_request(request))

                    return Response({"message":f"لایه رستری با موفقیت حذف شد"} , status=status.HTTP_200_OK)
                except OSError as e:
                    print(f"Error: {layer_raster_dir} : {e.strerror}")
                    return Response({"message":f"خطا در حذف فایل لایه رستری"} , status=status.HTTP_400_BAD_REQUEST)
            else:
                print(f"Directory '{layer_raster_dir}' does not exist.")
                return Response({"message":f"خطا در حذف لایه رستری"} , status=status.HTTP_400_BAD_REQUEST)
            

        except ShrhLayer.DoesNotExist:
            return Response(
                {"detail": "لایه شرح خدماتی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        except Exception as e:
            print(f"Error in RasterLayerApiview: {e}")
            return Response(
                {"detail": "خطا در بارگذاری لایه رستری"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DownloadRasterLayerApiView(APIView):
    """
    Download A Raster LAyer
        - Get sharkhadamatLayer id from body of request
        - Check user Allow Permmisson to this sharkhadamatLayer
        
        - Check sharkhadamatLayer.is_uploaded True & sharkhadamatLayer.raster_uuid have value
        - Check the /Raster_root/harkhadamatLayer.raster_uuid/ directory file in it exist
        - Return the Raster File
    """
    permission_classes = [HasDynamicPermission , HasShrhLayerAccess]

    class DownloadRasterLayerInputSerializer(serializers.Serializer):
        shrhlyr_id = serializers.IntegerField(
            required=True,
            allow_null=False
        )
        def validate_shrhlyr_id(self, value):
            if value <= 0:
                raise serializers.ValidationError("شناسه لایه باید عددی بزرگ‌تر از صفر باشد.")
            return value
        
    def post(self , request:Request) -> Response:
        try:
            serializer = self.DownloadRasterLayerInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data
            
            shrhlyr_id = validated_data['shrhlyr_id']

            shrh_layer_instance : ShrhLayer = ShrhLayer.objects.get(pk=shrhlyr_id)

            # HasShrhLayerAccess do this 
            # if not user.is_superuser and not user.has_sharhlayer_access(shrh_layer_instance):
            #     return Response({"detail": "کاربر به این لایه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)

            if shrh_layer_instance.layer_name.geometrytype != "raster":
                return Response(
                    {"detail": "این api برای لایه های غیر رستری قابل استفاده نیست"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if shrh_layer_instance.raster_uuid is None and not shrh_layer_instance.is_uploaded:
                return Response(
                    {"detail": "لایه مورد نظر از موجود نمیباشد."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            main_raster_dir = settings.RASTER_ROOT

            layer_raster_dir = os.path.join(main_raster_dir, str(shrh_layer_instance.raster_uuid))

            # Check if the directory exists before attempting to delete it
            if not os.path.exists(layer_raster_dir):
                return Response(
                    {"details":f"فایل لایه رستری موجود نمیباشد"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            cog_file_path = os.path.join(layer_raster_dir, "output_cog.tif")
            if not os.path.exists(cog_file_path):
                return Response(
                    {"detail": "فایل رستری یافت نشد"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            file_size = os.path.getsize(cog_file_path)
            
            # Create file response
            response = FileResponse(
                open(cog_file_path, 'rb'),
                as_attachment=True,
                content_type='image/tiff'
            )

            """
            response['X-Accel-Redirect'] Nginx intercept the response (handle file response itself)
            must add this to nginx
            
            location /protectedraster/ {
                internal;  # Only Django can trigger this
                alias /home/jazi/Work/zarrin/raster/;  # Notice trailing slash
                expires 1d;
                add_header Cache-Control "public, immutable";
            }
            """
            
            # Add additional headers
            response['Content-Type'] = 'image/tiff'
            response['Content-Disposition'] = f'attachment; filename="{shrh_layer_instance.raster_uuid}"'
            response['X-Accel-Redirect'] = f"/protectedraster/{shrh_layer_instance.raster_uuid}/output_cog.tif"
            response['Content-Length'] = file_size
            response['X-File-Size'] = file_size
            response['X-Layer-Name'] = shrh_layer_instance.raster_uuid

            return response
            

        except ShrhLayer.DoesNotExist:
            return Response(
                {"detail": "لایه شرح خدماتی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        except Exception as e:
            print(f"Error in RasterLayerApiview: {e}")
            return Response(
                {"detail": "خطا در دانلود لایه رستری"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class VerifyLayerApiView(APIView):
    """
        verify a layer 
    """
    permission_classes = [HasDynamicPermission , HasShrhLayerAccess]

    class VerifyLayerInputSerializer(serializers.Serializer):
        shrhlyr_id = serializers.IntegerField(
            required=True,
            allow_null=False
        )
        action = serializers.ChoiceField(
            choices=["verify", "unverify"],
            required=True,
            error_messages={
                "invalid_choice": "مقدار انتخابی معتبر نیست. فقط 'verify' یا 'unverify' مجاز است.",
                "required": "انتخاب عملیات (verify یا unverify) الزامی است.",
                "blank": "این فیلد نمی‌تواند خالی باشد.",
            },
        )
        def validate_shrhlyr_id(self, value):
            if value <= 0:
                raise serializers.ValidationError("شناسه لایه باید عددی بزرگ‌تر از صفر باشد.")
            return value
        
    def post(self, request: Request) -> Response:
        try:
            serializer = self.VerifyLayerInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user: User = request.user
            validated_data = serializer.validated_data
            shrhlyr_id = validated_data["shrhlyr_id"]
            action = validated_data["action"]

            try:
                shrh_layer_instance: ShrhLayer = ShrhLayer.objects.get(pk=shrhlyr_id)
            except ShrhLayer.DoesNotExist:
                return Response(
                    {"detail": "لایه شرح خدماتی با این آیدی وجود ندارد"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            
            # HasShrhLayerAccess do this 
            # if not user.is_superuser and not user.has_sharhlayer_access(shrh_layer_instance):
            #     return Response({"detail": "کاربر به این لایه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)

            # --- Condition 1: only superuser OR controller can verify ---
            if action == "verify":
                # if not (user.is_superuser or getattr(user, "is_controller", False)):
                #     return Response(
                #         {"details": "شما اجازه تایید لایه را ندارید"},
                #         status=status.HTTP_403_FORBIDDEN,
                #     )

                if not shrh_layer_instance.can_be_verified:
                    return Response(
                        {"details": "این لایه شرایط لازم برای تایید را ندارد"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                shrh_layer_instance.verify(user)
                return Response(
                    {"details": "لایه با موفقیت تایید شد"},
                    status=status.HTTP_200_OK,
                )

            # --- Condition 2: only superuser can unverify ---
            elif action == "unverify":
                if not user.is_superuser:
                    return Response(
                        {"details": "شما اجازه لغو تایید لایه را ندارید لطفا با پشتیبانی تماس بگیرید"},
                        status=status.HTTP_403_FORBIDDEN,
                    )

                if not shrh_layer_instance.is_verified:
                    return Response(
                        {"details": "این لایه تایید نشده است"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                shrh_layer_instance.is_verified = False
                shrh_layer_instance.verified_by = None
                shrh_layer_instance.verified_at = None
                shrh_layer_instance.save(
                    update_fields=["is_verified", "verified_by", "verified_at"]
                )

                return Response(
                    {"details": "تایید لایه با موفقیت لغو شد"},
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            print(f"Error in VerifyLayerApiView: {e}")
            return Response(
                {"detail": "خطا در تایید یا لغو تایید لایه"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LayerFeatureDetails(APIView):
    """
        GET: 
            1. get sharhlayer id from url param
            2. check user perm to this layer
            3. check layer is vector
            4. found table from shrhlayer -> layername
            4. query on table filter sharhlayer of it
            5. dynamically serialized 
            6. response to user
    
    """
    permission_classes = [HasDynamicPermission , HasShrhLayerAccess]

    class DynamicFeaturesListOutputserializer(serializers.ModelSerializer):
        class Meta:
            model = None
            # fields = '__all__'
            exclude = ('border', 'shr_layer')

    def get(self, request: Request, shrhlayerid:int) -> Response:
        try:
            shrh_layer_instance : ShrhLayer = ShrhLayer.objects.get(pk=shrhlayerid)

            if shrh_layer_instance.layer_name.geometrytype == "raster":
                return Response(
                    {"detail": "این api برای لایه های رستری قابل استفاده نیست"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            layer_model = get_model_from_string(model_app_label=LayersConfig.name ,
                                                model_class_name=shrh_layer_instance.layer_name.layername_en)
            
            print(">>>>>>>>>>>>>>>>" , layer_model)
            
            if layer_model is None:
                return Response(
                    {"detail": "جدول لایه مورد نظر یافت نشد"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            all_features = layer_model.objects.filter(shr_layer=shrh_layer_instance).all()
            
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(all_features, request)
            
            self.DynamicFeaturesListOutputserializer.Meta.model = layer_model

            serializer = self.DynamicFeaturesListOutputserializer(
                paginated_queryset,
                many=True,
                context={'request': request}
                )
            return paginator.get_paginated_response(serializer.data)

        except ShrhLayer.DoesNotExist:
            return Response(
                {"detail": "لایه شرح خدماتی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error in LayerFeatureDetails: {e}")
            return Response(
                {"detail": "خطا در خواندن فیچرهای لایه"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class GetListLayersFromGeodbFile(APIView):
    """
    API to get all layers from zipped GeoDatabase 
    """
    permission_classes = [IsAuthenticated]

    class GetListLayersFromGeodbFileInputSerializer(serializers.Serializer):
        gdbzipfile = serializers.FileField(required=True,
            help_text="ZIP file containing the gdb file",
            error_messages={
                'required': "این فیلد اجباری است",
                'blank': "این فیلد نمیتواند خالی باشد.",
                'null': "این فیلد نمیتواند null باشد."
            })
          
        def validate_gdbzipfile(self,value):
            if not zipfile.is_zipfile(value):
                raise serializers.ValidationError("فایل باید از نوع ZIP باشد.")
            
    def post(self, request:Request) -> Response:
        """
        get a zip file in requst files 
        get gdb from fille after unzip the file
        get all layers from zipped file and return it in Response 
        """

        input_serializer = self.GetListLayersFromGeodbFileInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        gdbzipfile = request.FILES['gdbzipfile']

        try:
            all_layer_list_with_value = get_layersnames_from_zipped_geodatabase_fast(gdb_zip_file=gdbzipfile)

            if len(all_layer_list_with_value) < 1:
                return Response({"detail": f"هیچ لایه با رکوردی در ژیودیتابیس ورودی یافت نشد"}, status=status.HTTP_400_BAD_REQUEST)

            dir_uuid = save_gdbzipfile_into_tempdir_with_uuid(gdb_zip_file=gdbzipfile)

            return Response({
                "layers": all_layer_list_with_value,
                "uuid": dir_uuid,
            }, status=status.HTTP_200_OK)
        
        except GeoDatabaseValidationError as gdderr:
            return Response({"detail": f"{str(gdderr)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UploadVectorLayerFromGdbApiView(APIView):
    """
    Upload New Layers From GeoDataBase
    - Get << uuid >> of uploaded zip gdb 
    - Get selected << sharlayer ids >> in array of intigers
    - Compare Selected shrlayers with layer of gdb Via
         sharlayer.layer_name.layername_en == layername in gdb file
    -
    """

    permission_classes = [HasDynamicPermission,]

    class VectorLayerInputSerializer(serializers.Serializer):
        selected_shrhlyr_ids = serializers.ListField(
            child=serializers.IntegerField(),
            required=True,
            help_text="لیستی از لایه های انتخاب شده برای بارگذاری",
            error_messages={
                'required': "این فیلد اجباری است",
                'blank': "این فیلد نمیتواند خالی باشد.",
                'null': "این فیلد نمیتواند null باشد."
            }
        )

        uuid = serializers.CharField(required=True,
            help_text="uuid is file path uuid",
            error_messages={
                'required': "این فیلد اجباری است",
                'blank': "این فیلد نمیتواند خالی باشد.",
                'null': "این فیلد نمیتواند null باشد."
            }
        )
        def validate_selected_shrhlyr_ids(self, value):
            for shrhlyr in value:
                if shrhlyr <= 0:
                    raise serializers.ValidationError("شناسه لایه باید عددی بزرگ‌تر از صفر باشد.")
            return value
        
    
    def post(self , request:Request) -> Response:
        from django.db.models.functions import Lower
        try:
            user = request.user
            serializer = self.VectorLayerInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data
            selected_shrhlyr_ids = validated_data['selected_shrhlyr_ids']
            inputuuid = validated_data['uuid']

            all_avalible_layers_in_gdb = read_all_layers_from_uuid_fast(geodb_uuid=inputuuid)
            all_avalible_layers_in_gdb_lower = [x.lower() for x in all_avalible_layers_in_gdb]

            print("all_avalible_layers_in_gdb>>>>>" , all_avalible_layers_in_gdb)
            
            sharlayer_instances = ShrhLayer.objects.filter(pk__in=selected_shrhlyr_ids)
            
            print("sharlayer_instances>>>>>>>>>" , sharlayer_instances)
            
            if not sharlayer_instances.exists():
                return Response({"detail":"لایه هایی با این شناسه ها یافت نشد"} , status=status.HTTP_400_BAD_REQUEST)

            # filtered_sharlayer_instances = sharlayer_instances.filter(layer_name__layername_en__in=all_avalible_layers_in_gdb)
            filtered_sharlayer_instances = sharlayer_instances.annotate(
                name_lower=Lower("layer_name__layername_en")
            ).filter(name_lower__in=all_avalible_layers_in_gdb_lower)
            
            print("filtered_sharlayer_instances>>>>>" , filtered_sharlayer_instances)
            
            # not_exist_layers_in_gdb = sharlayer_instances.exclude(layer_name__layername_en__in=all_avalible_layers_in_gdb)
            not_exist_layers_in_gdb = sharlayer_instances.annotate(
                name_lower=Lower("layer_name__layername_en")
            ).exclude(name_lower__in=all_avalible_layers_in_gdb_lower)

            print("not_exist_layers_in_gdb>>>>>" , not_exist_layers_in_gdb)

            if not_exist_layers_in_gdb.exists():
                layernames_fa = [lyr.layer_name.layername_fa for lyr in not_exist_layers_in_gdb]
                return Response({"detail":f"لایه های {",".join(layernames_fa)} در ژیودیتابیس ورودی برای بارگذاری یافت نشدند"} , status=status.HTTP_400_BAD_REQUEST)
            
            # Validate sharhlayer instances
            for shrhlyr in filtered_sharlayer_instances:

                if not user.is_superuser and not user.has_sharhlayer_access(shrhlyr):
                    return Response({"detail": f"کاربر به لایه {shrhlyr.layer_name.layername_fa} دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)

                if shrhlyr.is_verified:
                    return Response(
                    {"detail": f"لایه {shrhlyr.layer_name.layername_fa} تایید نهایی شده است و اجازه بارگذاری مجدد آن را ندارید"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

                if shrhlyr.layer_name.geometrytype == "raster":
                    return Response(
                        {"detail": f"این api برای لایه {shrhlyr.layer_name.layername_fa} رستری قابل استفاده نیست"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
            # Get All Layer models
            all_layer_models = []
            for shrhlyr in filtered_sharlayer_instances:
                
                layer_model = get_model_from_string(model_app_label=LayersConfig.name ,
                                                    model_class_name=shrhlyr.layer_name.layername_en)
                if layer_model is None:
                    return Response(
                        {"detail": f"جدول لایه {shrhlyr.layer_name.layername_fa} مورد نظر یافت نشد"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if not issubclass(layer_model, LinkedToLayerTable):
                    raise Exception("layer model is not LinkedToLayerTable instance")
                
                if layer_model.objects.filter(shr_layer=shrhlyr).exists():
                    return Response(
                        {"detail": "لایه مورد نظر از قبل موجود می‌باشد؛ در صورت تمایل، ابتدا آن را حذف و سپس بارگذاری مجدد نمایید."}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                print("layer_model.__name__>>>>>>",layer_model.__name__)
                
                all_layer_models.append(layer_model)

            result , data , message = process_layer_data_from_gdb(
                geodb_uuid = inputuuid,
                layer_models = all_layer_models,
                shrh_layer_instances = filtered_sharlayer_instances,
            )

            if not result:
                return Response({"detail":message }, status=status.HTTP_400_BAD_REQUEST)
            
            if not data:
                raise Exception("there is no data return from process_layer_data_from_gdb function")

            #process layers data (MULTI) if successful
            with transaction.atomic():
                for lyrdata in data:
                    print("data" , lyrdata)
                    shrhlyr = lyrdata.get('shrhlyr',None)
                    if not shrhlyr:
                        raise Exception('there is no shrhlyr in res result')
                    
                    lyrdatarows = lyrdata.get('rows',None)
                    if not lyrdatarows:
                        continue

                    this_lyr_layer_model = get_model_from_string(model_app_label=LayersConfig.name ,
                                                    model_class_name=shrhlyr.layer_name.layername_en)
                    
                    if not this_lyr_layer_model:
                        return Response(
                            {"detail": f"جدول لایه {shrhlyr.layer_name.layername_fa} مورد نظر یافت نشد"}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    instances = [this_lyr_layer_model(**item) for item in lyrdatarows]
                    layer_creation_result = this_lyr_layer_model.objects.bulk_create(instances)
                    
                    # Mark_as_uploaded is in model class 
                    shrhlyr.mark_as_uploaded(user)

                    #Send Notification
                    NotificationFactory.for_layer_upload(uploader_user=request.user,sharhlayer=shrhlyr)

            layernames = [lyr.layer_name.layername_fa for lyr in filtered_sharlayer_instances]

            return Response({"detail":f"لایه‌های {",".join(layernames)} با موفقیت بارگذاری شدند"} , status=status.HTTP_200_OK)

        except GeoDatabaseValidationError as gdderr:
            return Response(
                {"detail": f"{str(gdderr)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except FileNotFoundError as fee:
            return Response(
                { "detail":f'{str(fee)}' },
                status=status.HTTP_404_NOT_FOUND
            )
        
        except ShrhLayer.DoesNotExist:
            return Response(
                {"detail": "لایه شرح خدماتی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        except Exception as e:
            print(f"Error in UploadVectorLayerFromGdbApiView: {e}")
            return Response(
                {"detail": "خطا در بارگذاری لایه ها"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DownloadVectorLayer(APIView):
    """
        download vector layer from sharh layer instance
    
    """
    permission_classes = [HasDynamicPermission , HasShrhLayerAccess]

    def post(self, request:Request , shrhlayerid:int) -> Response:
        try:
            shrh_layer_instance : ShrhLayer = ShrhLayer.objects.get(pk=shrhlayerid)

            if shrh_layer_instance.layer_name.geometrytype == "raster":
                return Response(
                    {"detail": "این api برای لایه های رستری قابل استفاده نیست"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            layer_model = get_model_from_string(model_app_label=LayersConfig.name ,
                                                model_class_name=shrh_layer_instance.layer_name.layername_en)
            
            if layer_model is None:
                return Response(
                    {"detail": "جدول لایه مورد نظر یافت نشد"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            queryset =  layer_model.objects.filter(shr_layer=shrh_layer_instance).all()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            zip_path = queryset_to_shapefile(
                queryset=queryset,
                geometry_field="border",
                zip_output=True,
                filename=f"{str.lower(shrh_layer_instance.layer_name.layername_en)}_{timestamp}",
            )

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
        except ShrhLayer.DoesNotExist:
            return Response(
                {"detail": "لایه شرح خدماتی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error in LayerFeatureDetails: {e}")
            return Response(
                {"detail": "خطا در خواندن فیچرهای لایه"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class DownloadContractBorderVectorLayers(APIView):
    """
        download all vector layers of a contract border, bundled into a single zip
    """
    permission_classes = [HasDynamicPermission, HasShrhLayerAccess]

    def post(self, request: Request, contractborderid: uuid.UUID) -> Response:
        try:
            contract_border_instance = ContractBorder.objects.get(pk=contractborderid)
        except ContractBorder.DoesNotExist:
            return Response(
                {"detail": "محدوده قرارداد با این آیدی وجود ندارد"},
                status=status.HTTP_404_NOT_FOUND
            )

        shrh_layers = contract_border_instance.rcontractborderlayers.select_related("layer_name").all()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        shp_dirs = []  # raw per-layer shapefile folders, to be merged into one zip

        try:
            for shrh_layer_instance in shrh_layers:
                if shrh_layer_instance.layer_name.geometrytype == "raster":
                    continue

                layer_model = get_model_from_string(
                    model_app_label=LayersConfig.name,
                    model_class_name=shrh_layer_instance.layer_name.layername_en,
                )

                if layer_model is None:
                    continue

                queryset = layer_model.objects.filter(shr_layer=shrh_layer_instance).all()

                if not queryset.exists():
                    continue  # queryset_to_shapefile raises on empty querysets, so skip up front

                try:
                    shp_path = queryset_to_shapefile(
                        queryset=queryset,
                        geometry_field="border",
                        zip_output=False,
                        filename=f"{str.lower(shrh_layer_instance.layer_name.layername_en)}_{timestamp}",
                    )
                    shp_dirs.append(os.path.dirname(shp_path))
                except Exception as e:
                    print(f"Skipping layer {shrh_layer_instance.pk} ({shrh_layer_instance.layer_name.layername_en}): {e}")
                    continue

            if not shp_dirs:
                return Response(
                    {"detail": "هیچ لایه قابل خروجی برای این محدوده قرارداد یافت نشد"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            zip_basename = f"contractborder_{contractborderid}_{timestamp}"
            zip_path = os.path.join(settings.MEDIA_ROOT, f"{zip_basename}.zip")

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for shp_dir in shp_dirs:
                    layer_folder = os.path.basename(shp_dir)  # keep each layer's parts grouped inside the zip
                    for part in os.listdir(shp_dir):
                        zf.write(
                            os.path.join(shp_dir, part),
                            arcname=os.path.join(layer_folder, part),
                        )

            for shp_dir in shp_dirs:
                shutil.rmtree(shp_dir, ignore_errors=True)

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
            print(f"Error in DownloadContractBorderVectorLayers: {e}")
            return Response(
                {"detail": "خطا در خواندن فیچرهای لایه"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class SingleFeatureDetailsApiView(APIView):
    """
        GET:
            For One Feature Details Dynamically serializer and response
        Put:
            Edit only none geometry fields for each one dynamically
    """

    class DynamicSingleFeaturesDetailsOutputserializer(serializers.ModelSerializer):
        class Meta:
            model = None
            exclude = ('border', 'shr_layer')

    class DynamicSingleFeaturesDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = None
            exclude = ('id', 'border', 'shr_layer')

    def get(self , request:Request, shrhlyr_id:int , feature_id:int)->Response:
        try:
            thisuser = request.user
            shrhlayer_instance : ShrhLayer = ShrhLayer.objects.get(pk=shrhlyr_id)

            if not thisuser.is_superuser and not thisuser.has_sharhlayer_access(sharhlayer=shrhlayer_instance):
                return Response({"detail":"شما به این لایه شرح خدماتی دسترسی ندارید"},status=status.HTTP_400_BAD_REQUEST)
                            
            if feature_id <= 0:
                return Response({"detail": "شناسه عارضه معتبر نیست"}, status=status.HTTP_400_BAD_REQUEST)

            layername = shrhlayer_instance.layer_name.layername_en
            model_class : DjangoModel = get_model_from_string(
                                            model_app_label=LayersConfig.name,
                                            model_class_name=layername
                                        )
            
            print("model class>>>>>" , model_class)
            
            feature_instance = model_class.objects.get(pk=feature_id)
            
            self.DynamicSingleFeaturesDetailsOutputserializer.Meta.model = model_class

            serializer_data = self.DynamicSingleFeaturesDetailsOutputserializer(feature_instance,many=False,)

            return Response(serializer_data.data,status=status.HTTP_200_OK)

        except ShrhLayer.DoesNotExist:
            return Response(
                {"detail": "لایه شرح خدماتی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except model_class.DoesNotExist:
            return Response(
                {"detail": "عارضه ایی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error in SingleFeatureDetailsApiView: {e}")
            return Response(
                {"detail": "خطا در خواندن یک فیچر لایه"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self , request:Request, shrhlyr_id:int , feature_id:int)->Response:
        try:
            thisuser = request.user
            shrhlayer_instance: ShrhLayer = ShrhLayer.objects.get(pk=shrhlyr_id)

            if not thisuser.is_superuser and not thisuser.has_sharhlayer_access(sharhlayer=shrhlayer_instance):
                return Response({"detail": "شما به این لایه شرح خدماتی دسترسی ندارید"}, status=status.HTTP_400_BAD_REQUEST)

            if feature_id <= 0:
                return Response({"detail": "شناسه عارضه معتبر نیست"}, status=status.HTTP_400_BAD_REQUEST)

            layername = shrhlayer_instance.layer_name.layername_en
            model_class: DjangoModel = get_model_from_string(
                model_app_label=LayersConfig.name,
                model_class_name=layername
            )

            feature_instance = model_class.objects.get(pk=feature_id)

            self.DynamicSingleFeaturesDetailsInputSerializer.Meta.model = model_class

            serializer = self.DynamicSingleFeaturesDetailsInputSerializer(
                feature_instance,
                data=request.data,
                partial=True,  # only fields sent are updated; geometry fields are excluded anyway
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            self.DynamicSingleFeaturesDetailsOutputserializer.Meta.model = model_class
            output_serializer = self.DynamicSingleFeaturesDetailsOutputserializer(feature_instance)

            return Response(output_serializer.data, status=status.HTTP_200_OK)

        except ShrhLayer.DoesNotExist:
            return Response(
                {"detail": "لایه شرح خدماتی با این آیدی وجود ندارد"},
                status=status.HTTP_404_NOT_FOUND
            )
        except model_class.DoesNotExist if model_class else Exception:
            return Response(
                {"detail": "عارضه ایی با این آیدی وجود ندارد"},
                status=status.HTTP_404_NOT_FOUND
            )
        except serializers.ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error in FeatureDetailsApiView PUT: {e}")
            return Response(
                {"detail": "خطا در ویرایش فیچر لایه"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
