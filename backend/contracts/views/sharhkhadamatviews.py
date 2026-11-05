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
from accounts.models import User
from contracts.models.models import (
    Contract,
)
from contracts.models.SharhKhadamats import (
    ShrhBase,
    ShrhLayer,
)
from layers.models.models import (
    LayersNames,
)
from common.mixins import SearchMixin

delete_logger = logging.getLogger('delete_activity_logger')

class SharhkhadamatListApiView(SearchMixin , APIView):
    """
        ****** Get A Contract id from url ! ****** 
        GET: Return List of All Sharh_base associated with the Contract
        POST: Create new shrh_base instance for the Contract
    """
    # look at SearchMixin its come from there !
    search_fields = ['title' ,]

    class SharhkhadamatListOutputSerializer(serializers.ModelSerializer):

        class Meta:
            model = ShrhBase
            fields = ['id' ,'title','percentage',
                'worked_percentage','contract','faz',
                'completion_percentage','remaining_percentage',
                'total_price','completed_price']
            
    class SharhkhadamatListInputSerializer(serializers.ModelSerializer):
        def validate(self, data):
            percentage = data.get('percentage')

            if percentage is not None:
                if percentage < 0 or percentage > 100:
                    raise serializers.ValidationError({
                        'weight': 'مقدار درصد باید بین ۰ تا ۱۰۰ باشد'
                    })
            return data
        class Meta:
            model = ShrhBase
            fields = ['title','percentage','faz',
                      'worked_percentage',]
            
    def get(self , request:Request , contractid:str) -> Response:
        try:
            user : User = request.user 
            contract_instance = Contract.objects.get(pk=contractid)
            if not user.is_superuser and not user.has_contract_access(contract_instance):
                return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            all_shar_base = ShrhBase.objects.filter(contract=contract_instance)
            # Add Search query param to it
            all_shar_base = self.apply_search(all_shar_base, request)

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(all_shar_base, request)            
            serializer = self.SharhkhadamatListOutputSerializer(paginated_queryset,many=True)
            return paginator.get_paginated_response(serializer.data)
        except Contract.DoesNotExist:
            return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self , request:Request , contractid:str) -> Response:
        try:
            user : User = request.user 
            contract_instance = Contract.objects.get(pk=contractid)
            if not user.is_superuser and not user.has_contract_access(contract_instance):
                return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            input_serializer = self.SharhkhadamatListInputSerializer(data=request.data)
            if input_serializer.is_valid():
                shrh_instance = input_serializer.save(contract=contract_instance)
                output_serializer = self.SharhkhadamatListOutputSerializer(shrh_instance)
                return Response(output_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Contract.DoesNotExist:
            return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ساخت شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

class SharhkhadamatDetailApiView(APIView):
    """
        ***** Get A Shar_base id from url ! *****
        **** Get A Contract id from url ! ****
        *** check the Contract exist or not! ***
        GET: Retrive An instance Sharh_base associated with the Contract
        PUT: Update An instance Sharh_base associated with the Contract
        Delete: Delete An instance Sharh_base associated with the Contract
    """
    class SharhkhadamatDetaiOutputSerializer(serializers.ModelSerializer):

        class Meta:
            model = ShrhBase
            fields = ['id' ,'title','percentage',
                'worked_percentage','contract','faz',
                'completion_percentage','remaining_percentage',
                'total_price','completed_price']
        
    class SharhkhadamatDetailInputSerializer(serializers.ModelSerializer):
        def validate(self, data):
            # Get new or existing values
            percentage = data.get('percentage', getattr(self.instance, 'percentage', None))

            # Validation: weight must be between 0 and 100
            if percentage is not None:
                if percentage < 0 or percentage > 100:
                    raise serializers.ValidationError({
                        'percentage': 'مقدار درصد باید بین ۰ تا ۱۰۰ باشد'
                    })

            return data
        class Meta:
            model = ShrhBase
            fields = ['title','percentage','faz',
                      'worked_percentage',]
    def get(self , request:Request , contractid:str , shrhbaseid:int) -> Response:
        try:
            user:User = request.user
            contract_instance = Contract.objects.get(pk=contractid)
            if not user.is_superuser and not user.has_contract_access(contract_instance):
                return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            shar_base_instance = ShrhBase.objects.get(pk=shrhbaseid)
            # Check SharhBase belongs to the Contract
            if shar_base_instance.contract_id != contract_instance.id: # type: ignore
                return Response({"detail": "این شرح خدمات متعلق به این قرارداد نیست"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.SharhkhadamatDetaiOutputSerializer(shar_base_instance,many=False)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except Contract.DoesNotExist:
            return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except ShrhBase.DoesNotExist:
            return Response({"detail":"شرح خدماتی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self , request:Request , contractid:str , shrhbaseid:int) -> Response:
        try:
            user:User = request.user
            contract_instance = Contract.objects.get(pk=contractid)
            if not user.is_superuser and not user.has_contract_access(contract_instance):
                return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            shar_base_instance = ShrhBase.objects.get(pk=shrhbaseid)
            if shar_base_instance.contract_id != contract_instance.id: # type: ignore
                return Response({"detail": "این شرح خدمات متعلق به این قرارداد نیست"}, status=status.HTTP_400_BAD_REQUEST)
            input_serializer = self.SharhkhadamatDetailInputSerializer(
                shar_base_instance,
                data=request.data,
                partial=True
            )
            if input_serializer.is_valid():
                updated_instance = input_serializer.save()
                output_serializer = self.SharhkhadamatDetaiOutputSerializer(updated_instance)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
        except Contract.DoesNotExist:
            return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except ShrhBase.DoesNotExist:
            return Response({"detail":"شرح خدماتی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self , request:Request , contractid:str , shrhbaseid:int) -> Response:
        try:
            user:User = request.user
            contract_instance = Contract.objects.get(pk=contractid)
            if not user.is_superuser and not user.has_contract_access(contract_instance):
                return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            shar_base_instance = ShrhBase.objects.get(pk=shrhbaseid)
            if shar_base_instance.contract_id != contract_instance.id: # type: ignore
                return Response({"detail": "این شرح خدمات متعلق به این قرارداد نیست"}, status=status.HTTP_400_BAD_REQUEST)
            shar_base_instance.delete()
            delete_logger.warning(f"حذف بند شرح خدمات {shar_base_instance.title}" , extra=get_details_from_request(request))
            return Response(status=status.HTTP_204_NO_CONTENT)           
        except Contract.DoesNotExist:
            return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except ShrhBase.DoesNotExist:
            return Response({"detail":"شرح خدماتی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SharhKhadamatLayerListApiView(SearchMixin, APIView):
    """
        Get A Contract uuid from url 
        GET: List of all sharh_layers associated to this Contract base with Shar_base title Seprated
        
        POST: Creates one or more sharh_layers instances.
            (Input can be a single object or a list of objects.)
        
        ****** This endpoint is exclusively for the Admin Page;
          it doesn't handle user layers or the layer upload form.
          (Those URLs are in the layers app, not here.) ******

    """
    search_fields = ['shrh_base__title',
                'layer_name__lyrgroup_en',
                'layer_name__lyrgroup_fa',
                'layer_name__layername_en',
                'layer_name__layername_fa',]
    class SharhKhadamatLayerListOutputSerializer(serializers.ModelSerializer):
        class SharhKhadamatLayerListLayername(serializers.ModelSerializer):
            class Meta:
                model = LayersNames
                fields = ['id','dtyp','lyrgroup_en','lyrgroup_fa',
                          'layername_en','layername_fa','geometrytype']
        class SharhKhadamatLayerListUser(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ['id','username','first_name_fa','last_name_fa']

        class SharhkhadamatLayerListShrBase(serializers.ModelSerializer):
            class Meta:
                model = ShrhBase
                fields = ["id","title"]

                
        layer_name = SharhKhadamatLayerListLayername()
        verified_by = SharhKhadamatLayerListUser()
        shrh_base = SharhkhadamatLayerListShrBase()
        last_uploaded_by = SharhKhadamatLayerListUser()

        class Meta:
            model = ShrhLayer
            fields = ['id','shrh_base','layer_name','raster_uuid','scale','is_uploaded','status',
                'unit','unit_price',
                'last_uploaded_date','last_uploaded_by','upload_count','is_verified','verified_by','verified_at',
                'layer_weight','layer_volume',]
            
    class SharhKhadamatLayerListInputSerializer(serializers.ModelSerializer):

        class Meta:
            model = ShrhLayer
            fields = ['shrh_base','layer_name','scale','unit','unit_price',
                    'layer_weight','layer_volume',]
            
    def _build_filters(self, request: Request, contractid: str) -> dict:
        """Build filter dictionary from URL params and query params"""
        filters = {
            'shrh_base__contract_id': contractid
        }
        
        # Add sharhbase filter if provided
        sharhbase_id = request.query_params.get('sharhbase')
        if sharhbase_id:
            try:
                filters['shrh_base_id'] = int(sharhbase_id)
            except ValueError:
                raise ValidationError({"sharhbase": "شناسه شرح پایه معتبر نیست"})
        
        return filters
    
    def get(self , request:Request , contractid:str) -> Response:
        try:
            # Validate contract exists
            contract_instance = Contract.objects.get(pk=contractid)

            # Dose need check user acceess to this contract ???
            
            # Build filters from request
            filters = self._build_filters(request, contractid)
            
            # Get all ShrhLayer objects with applied filters
            shrh_layers = ShrhLayer.objects.filter(
                **filters
            ).select_related(
                'shrh_base', 
                'layer_name',
                'verified_by',
                'last_uploaded_by',
                'verified_by'
            ).order_by('shrh_base__title', 'layer_name__layername_en') 

            # Apply user permission filtering
            if not request.user.is_superuser:
                # Filter to only layers the user has access to
                shrh_layers = shrh_layers.filter(
                    accessible_by_users=request.user
            )

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(shrh_layers, request)
            serializer = self.SharhKhadamatLayerListOutputSerializer(paginated_queryset, many=True)

            return paginator.get_paginated_response(serializer.data)
        
        except Contract.DoesNotExist:
            return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
        return Response({"detail": "خطا در خواندن لایه‌های شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request: Request, contractid: str) -> Response:
        try:
            contract_instance = Contract.objects.get(pk=contractid)
        except Contract.DoesNotExist:
            return Response(
                {"detail": "قراردادی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": "خطا در یافتن قرارداد"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Handle both single object and list of objects
        data = request.data
        if not isinstance(data, list):
            data = [data]
        
        created_layers = []
        errors = []

        for index, layer_data in enumerate(data):
            # Create input serializer for validation
            input_serializer = self.SharhKhadamatLayerListInputSerializer(data=layer_data)
        
            if input_serializer.is_valid():
                try:
                    user: User = request.user
                    # Validate that shrh_base belongs to the contract
                    shrh_base = input_serializer.validated_data['shrh_base']
                    if shrh_base.contract != contract_instance:
                        errors.append({
                            'index': index,
                            'error': 'بند شرح خدمات به این قرارداد تعلق ندارد'
                        })
                        continue


                    # Check for duplicate layer (optional business logic) 
                    existing_layer = ShrhLayer.objects.filter(
                        shrh_base=shrh_base,
                        layer_name=input_serializer.validated_data['layer_name'], 
                        scale = input_serializer.validated_data['scale']
                    ).first()
                    
                    if existing_layer:
                        errors.append({
                            'index': index,
                            'error': 'لایه با این مشخصات قبلاً ایجاد شده است'
                        })
                        continue

                    new_layer = ShrhLayer.objects.create(
                        shrh_base=shrh_base,
                        layer_name=input_serializer.validated_data['layer_name'],
                        scale=input_serializer.validated_data.get('scale'),
                        layer_weight=input_serializer.validated_data.get('layer_weight', 0),
                        layer_volume=input_serializer.validated_data.get('layer_volume', 0),
                    )
                    created_layers.append(new_layer)
                    
                except ValidationError as v_error: #database validation error
                    # Handle Django ValidationError properly
                    error_message = str(v_error)
                    if hasattr(v_error, 'message_dict'):
                        error_message = v_error.message_dict
                    elif hasattr(v_error, 'messages'):
                        error_message = v_error.messages
                        
                    errors.append({
                        'index': index,
                        'error': error_message
                    })

                except Exception as create_error:
                    errors.append({
                        'index': index,
                        'error': f'خطا در ایجاد لایه: {str(create_error)}'
                    })
            else:
                errors.append({
                    'index': index,
                    'error': input_serializer.errors
                })

        # Grant access to all created layers at once (bulk operation)
        if created_layers:
            user.grant_bulk_sharhlayer_access(sharhlayers=created_layers)
        # Build response
        response_data = {}
        if created_layers:
            # Serialize created layers using output serializer
            output_serializer = self.SharhKhadamatLayerListOutputSerializer(
                created_layers, many=True
            )
            response_data['created_layers'] = output_serializer.data
            response_data['created_count'] = len(created_layers)
            
        if errors:
            response_data['errors'] = errors
            response_data['error_count'] = len(errors)
        
        # Determine response status
        if created_layers and not errors:
            # All successful
            return Response(response_data, status=status.HTTP_201_CREATED)
        elif created_layers and errors:
            # Partial success
            return Response(response_data, status=status.HTTP_207_MULTI_STATUS)
        else:
            # All failed
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class SharhKhadamatLayerDetailApiView(APIView):
    """
        Get A SharhLayer id from url 
        GET: Retrive An Instance of ShrhLayer Modal
        DELETE: GET An Instance of ShrhLayer And Delete it
        PUT: Dont have it yet !
        
        ****** This endpoint is exclusively for the Admin Page;
          it doesn't handle user layers or the layer upload form.
          (Those URLs are in the layers app, not here.) ******

    """
    class SharhKhadamatLayerDetailOutputSerializer(serializers.ModelSerializer):
        class SharhKhadamatLayerDetailLayername(serializers.ModelSerializer):
            class Meta:
                model = LayersNames
                fields = ['dtyp','lyrgroup_en','lyrgroup_fa',
                          'layername_en','layername_fa','geometrytype']
        class SharhKhadamatLayerDetailUser(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ['id','username','first_name_fa','last_name_fa']


                
        layer_name = SharhKhadamatLayerDetailLayername()
        verified_by = SharhKhadamatLayerDetailUser()
        last_uploaded_by = SharhKhadamatLayerDetailUser()

        class Meta:
            model = ShrhLayer
            fields = ['id','shrh_base','layer_name','raster_uuid','scale','is_uploaded','status',
                'unit','unit_price',
                'last_uploaded_date','last_uploaded_by','upload_count','is_verified','verified_by','verified_at',
                'scale','layer_weight','layer_volume',]
            
    class SharhKhadamatLayerDetailInputputSerializer(serializers.ModelSerializer):

        def validate(self, data):
            return data

        class Meta:
            model = ShrhLayer
            fields = ['scale','layer_weight',
                    'unit','unit_price',
                    'layer_volume',] 
            
    def get(self , request:Request , contractid:str ,shrhid:int) -> Response:
        try:
            user:User = request.user 
            contract_instance = Contract.objects.get(pk=contractid)
            #TODO make it better (check dhrbase exist and shrhlayer related to shrhbase)
            shrhlayer_instance = ShrhLayer.objects.get(pk=shrhid) 
            if not user.is_superuser and not user.has_sharhlayer_access(shrhlayer_instance):
                return Response({"detail": "کاربر به این لایه شرح خدمات دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            serializer = self.SharhKhadamatLayerDetailOutputSerializer(shrhlayer_instance)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except Contract.DoesNotExist:
            return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except ShrhLayer.DoesNotExist:
            return Response({"detail":"لایه شرح خدماتی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن لایه شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self , request:Request , contractid:str ,shrhid:int) -> Response:
        try:
            user:User = request.user 
            contract_instance = Contract.objects.get(pk=contractid)
            shrhlayer_instance = ShrhLayer.objects.get(pk=shrhid) 
            if not user.is_superuser and not user.has_sharhlayer_access(shrhlayer_instance):
                return Response({"detail": "کاربر به این لایه شرح خدمات دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            input_serializer = self.SharhKhadamatLayerDetailInputputSerializer(
                shrhlayer_instance,
                data=request.data,
                partial=True)
            if not input_serializer.is_valid():
                return Response(input_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            input_serializer.save()
            output_serializer = self.SharhKhadamatLayerDetailOutputSerializer(shrhlayer_instance)
            return Response(output_serializer.data , status=status.HTTP_200_OK)
        except Contract.DoesNotExist:
            return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except ShrhLayer.DoesNotExist:
            return Response({"detail":"لایه شرح خدماتی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن لایه شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
    def delete(self , request:Request , contractid:str ,shrhid:int) -> Response:
        try:
            user:User = request.user 
            contract_instance = Contract.objects.get(pk=contractid)
            #TODO make it better (check dhrbase exist and shrhlayer related to shrhbase)
            shrhlayer_instance = ShrhLayer.objects.get(pk=shrhid) 
            if not user.is_superuser and not user.has_sharhlayer_access(shrhlayer_instance):
                return Response({"detail": "کاربر به این لایه شرح خدمات دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            shrhlayer_instance.delete()
            delete_logger.warning(f"حذف لایه {shrhlayer_instance.id} از لایه های شرح خدمات" , extra=get_details_from_request(request))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Contract.DoesNotExist:
            return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except ShrhLayer.DoesNotExist:
            return Response({"detail":"لایه شرح خدماتی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در حذف لایه شرح خدمات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            