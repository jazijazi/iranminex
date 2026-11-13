import logging
from logs.utils import get_details_from_request
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
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
    ShrhCatalog,
)
from common.mixins import SearchMixin , FilterMixin

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
                "pk", "code", "title", "is_group", "order",
                "contract_domin", "contract_domin_title",
                "faz", "faz_title",
                "parent",
                "vahed", "vahed_title",
            ]

    class ShrhCatalogListInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ShrhCatalog
            fields = ["contract_domin", "code", "faz", "parent", "is_group", "title", "vahed", "description", "order"]

        def validate(self, attrs):
            """
            همان قوانین ShrhCatalog.clean() در سطح serializer، تا خطا به‌جای 500
            به‌صورت 400 برگردد.
            """
            parent = attrs.get("parent")
            faz = attrs.get("faz")
            is_group = attrs.get("is_group")
            vahed = attrs.get("vahed")

            errors = {}
            if parent:
                if not parent.is_group:
                    errors["parent"] = "والد باید یک گروه باشد."
                elif faz is None or parent.faz_id != faz.pk:
                    errors["faz"] = "فاز بند باید با فاز گروه والد یکی باشد."
            if is_group and vahed:
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
                "pk", "code", "title", "is_group", "description", "order",
                "contract_domin", "contract_domin_title",
                "faz", "faz_title",
                "parent",
                "vahed", "vahed_title",
            ]

    class ShrhCatalogDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ShrhCatalog
            fields = ["contract_domin", "code", "faz", "parent", "is_group", "title", "vahed", "description", "order"]

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
            is_group = get("is_group")
            vahed = get("vahed")

            errors = {}
            if parent:
                if parent.pk == self.instance.pk:
                    errors["parent"] = "یک بند نمی‌تواند والد خودش باشد."
                elif not parent.is_group:
                    errors["parent"] = "والد باید یک گروه باشد."
                elif faz is None or parent.faz_id != faz.pk:
                    errors["faz"] = "فاز بند باید با فاز گروه والد یکی باشد."
            if is_group and vahed:
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
            