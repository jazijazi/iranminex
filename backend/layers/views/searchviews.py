import os
import shutil
import json
from django.db.models.query import Q , QuerySet
from django.contrib.gis.geos import GEOSGeometry, GEOSException
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import serializers
from django.http import FileResponse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.validators import FileExtensionValidator
from common.pagination import CustomPagination
from django.conf import settings

from layers.utils import get_model_from_string
from layers.apps import LayersConfig

from common.services.notification_services import NotificationFactory

from accounts.models import User

from common.models import Province

from initialborders.models.models import (
    InitialBorder,
    InitialBorderDomin,
)


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
    convert_tif_to_cog_and_save_to_rasterdir
)

from accounts.permissions import (
    HasDynamicPermission,
    HasShrhLayerAccess,
)


class SearchLayerByLocation(APIView):
    """
        POST: 
          1. get geojson polygon from request body
          2. intersect with contractborders (or initialborder)
    """

    #permission is dynamic

    class SearchLayerByLocationInputSerializer(serializers.Serializer):
        query = serializers.JSONField(
            required=True,
            help_text="GeoJSON geometry (Feature, Point, LineString, or Polygon)"
        )
        distance_km = serializers.IntegerField(
            required=False,
            default=1,
            min_value=1,
            help_text="Distance in kilometers for Point/LineString queries"
        )
        
        def validate_query(self, value):
            """
            Validate that the query is a valid GeoJSON geometry
            """
            # Check if value is a dict
            if not isinstance(value, dict):
                raise serializers.ValidationError("query باید یک شی JSON باشد")
            
            # Check for required 'type' field
            if 'type' not in value:
                raise serializers.ValidationError("فیلد type در GeoJSON یافت نشد")
            
            geojson_type = value.get('type')
            
            # Reject FeatureCollection
            if geojson_type == "FeatureCollection":
                raise serializers.ValidationError("نوع FeatureCollection برای جستجو پشتیبانی نمیشود")
            
            # Extract geometry based on type
            if geojson_type == "Feature":
                geometry = value.get("geometry")
                if not geometry:
                    raise serializers.ValidationError("فیلد geometry در Feature یافت نشد")
            elif geojson_type in ["Point", "LineString", "Polygon"]:
                geometry = value
            else:
                raise serializers.ValidationError(
                    f"نوع GeoJSON '{geojson_type}' پشتیبانی نمی‌شود. فقط Feature, Point, LineString, Polygon پشتیبانی می‌شود"
                )
            
            # Validate geometry with GEOSGeometry
            try:
                geom = GEOSGeometry(json.dumps(geometry), srid=4326)
                
                supported_types = ['Point', 'LineString', 'Polygon']
                if geom.geom_type not in supported_types:
                    raise serializers.ValidationError(
                        f"فقط این انواع هندسی پشتیبانی میشود: {', '.join(supported_types)}"
                    )
            except (GEOSException, ValueError) as e:
                raise serializers.ValidationError(f"خطا در پردازش GeoJSON: {str(e)}")
            
            return value


    def post(self, request: Request) -> Response:
        # Validate input
        input_serializer = self.SearchLayerByLocationInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = input_serializer.validated_data
        geojson_data = validated_data['query']
        distance_km = validated_data['distance_km']
        
        try:
            user: User = request.user
            
            # Extract and convert geometry
            geometry = self._extract_geometry(geojson_data)
            geom = GEOSGeometry(json.dumps(geometry), srid=4326)
            
            # Get intersecting initial borders
            intersected_borders = self._get_intersected_borders(user, geom, distance_km)
            
            # Get accessible contract borders
            accessible_contract_borders = self._get_accessible_contract_borders(user)
            accessible_contract_ids = self._get_accessible_contract_ids(user)
            
            result = []
        
            for initial_border in intersected_borders:
                # Get contract borders for this initial border that user can access
                relevant_contract_borders = accessible_contract_borders.filter(
                    initborder=initial_border,
                    contract_id__in=accessible_contract_ids
                )
            
                all_layers = []
            
                for contract_border in relevant_contract_borders:
                    # Get sharh layers for this contract border
                    sharh_layers = self._get_sharh_layers(user, contract_border)
                    
                    # Add each sharh layer to all_layers list
                    for sharh_layer in sharh_layers:
                        all_layers.append({
                            "sharhlayerid": sharh_layer.id,
                            "contracttitle": contract_border.contract.title,
                            "layernameen": sharh_layer.layer_name.layername_en,
                            "layernamefa": sharh_layer.layer_name.layername_fa,
                            "layer": sharh_layer.layer_name.geometrytype,
                        })
            
                # Only add initial border if it has layers
                if all_layers:
                    result.append({
                        "initialborderid": initial_border.id,
                        "initialbordertitle": initial_border.title,
                        "alllayers": all_layers
                    })
        
            return Response(result, status=status.HTTP_200_OK)
            
        except GEOSException as e:
            print(str(e))
            return Response({"error": f"خطا در GeoJSON ورودی"}, 
                        status=status.HTTP_400_BAD_REQUEST)            
        except ValueError as e:
            print(str(e))
            return Response({"error": f"خطا در جستجو مکانی"}, 
                        status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return Response({"error": f"خطا در جستجو مکانی"}, 
                        status=status.HTTP_400_BAD_REQUEST)
        
    def _extract_geometry(self, geojson_data: dict) -> dict:
        """Extract geometry from GeoJSON data"""
        if geojson_data.get("type") == "Feature":
            return geojson_data.get("geometry")
        return geojson_data
    
    def _get_intersected_borders(
        self, 
        user: User, 
        geom: GEOSGeometry, 
        distance_km: int
    ) -> QuerySet[InitialBorder]:
        """Get initial borders that intersect with the geometry"""
        # Get base queryset based on user permissions
        if user.is_superuser:
            base_queryset = InitialBorder.objects.all()
        else:
            base_queryset = user.get_accessible_initialborder()
        
        base_queryset = base_queryset.prefetch_related(
            'province',
            'dtyp'
        ).select_related('dtyp')
        
        # Filter based on geometry type
        geom_type = geom.geom_type.lower()
        
        if geom_type == "polygon":
            return base_queryset.filter(
                Q(border__intersects=geom) & ~Q(border=None)
            ).distinct()
        
        elif geom_type in ["linestring", "point"]:
            distance_deg = float(distance_km / 111)  # Approximate km to degrees conversion
            return base_queryset.filter(border__dwithin=(geom, distance_deg))
        
        return InitialBorder.objects.none()
    
    def _get_accessible_contract_borders(self, user: User) -> QuerySet[ContractBorder]:
        """Get contract borders accessible to the user"""
        queryset = ContractBorder.objects.select_related(
            'contract__dtyp',
            'initborder'
        )
        
        if user.is_superuser:
            return queryset.all()
        
        return user.get_accessible_contractborders().select_related(
            'contract__dtyp',
            'initborder'
        )
    
    def _get_accessible_contract_ids(self, user: User) -> set:
        """Get IDs of contracts accessible to the user"""
        if user.is_superuser:
            return set(Contract.objects.values_list('id', flat=True))
        
        return set(user.get_accessible_contracts().values_list('id', flat=True))
    
    def _get_sharh_layers(
        self, 
        user: User, 
        contract_border: ContractBorder
    ) -> QuerySet[ShrhLayer]:
        """Get sharh layers for a contract border based on user permissions"""
        base_filter = Q(is_uploaded=True, contractborder=contract_border)
        prefetch = ['shrh_base', 'layer_name']
        
        if user.is_superuser:
            return ShrhLayer.objects.filter(base_filter).prefetch_related(*prefetch)
        
        return user.accessible_shrh_layers.filter(base_filter).prefetch_related(*prefetch)
        


#EXAMPLE 

#################### 1 ####################
# {
#   "type": "Feature",
#   "properties": {},
#   "geometry": {
#     "type": "Polygon",
#     "coordinates": [
#       [
#         [53.62154462646424, 27.074105990132722],
#         [56.2622898759698, 27.128041304265125],
#         [55.57944078462975, 29.40981747687617],
#         [51.48365376506362, 35.69132018119741],
#         [44.046637883115125, 35.370032077660426],
#         [48.351768733465406, 30.59360827198978],
#         [50.06490602193668, 30.372394144284456],
#         [53.62154462646424, 27.074105990132722]
#       ]
#     ]
#   }
# }

#################### 2 ####################
# {
#       "type": "Feature",
#       "properties": {},
#       "geometry": {
#         "type": "Polygon",
#         "coordinates": [
#           [
#             [
#               45.358844004931484,
#               37.08060809427454
#             ],
#             [
#               46.90101979291754,
#               35.15071895948276
#             ],
#             [
#               46.306175107810105,
#               33.47552524106044
#             ],
#             [
#               53.03159662175173,
#               33.78743111826863
#             ],
#             [
#               52.99167786250041,
#               36.55404921962396
#             ],
#             [
#               45.358844004931484,
#               37.08060809427454
#             ]
#           ]
#           ]
#       }
#  }

################ 3 #################
# {
#   "type": "Feature",
#   "properties": {},
#   "geometry": {
#     "coordinates": [
#       49.67128080620762,
#       34.074122577832185
#     ],
#     "type": "Point"
#   }
# }