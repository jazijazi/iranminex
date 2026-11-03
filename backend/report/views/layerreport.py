import uuid
from typing import cast, Dict, Any
from django.db.models import Count, Sum, Q, F, Case, When, DecimalField, ExpressionWrapper, FloatField , BigIntegerField
from django.db.models.functions import Coalesce
from django.core.validators import FileExtensionValidator
from django.contrib.gis.db.models.functions import Area, Transform
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import serializers
from django.db.models.expressions import RawSQL
from rest_framework.permissions import AllowAny , IsAdminUser
from common.pagination import CustomPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from django.db import transaction
from django.contrib.gis.geos import MultiPolygon
from common.models import Company , Province
from accounts.models import User

from layers.utils import get_model_from_string
from layers.apps import LayersConfig

from initialborders.models.models import (
    InitialBorder,
    InitialBorderDomin,
)
from contracts.models.models import (
    Contract,
    ContractDomin,
    ContractBorder,
    ShrhLayer,
    ShrhBase,
)
from layers.models.models import LayersNames
from common.models import Province , County

from django.db.models import Sum
from django.contrib.gis.db.models.functions import Area  # not required, kept RawSQL like your original
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.db.models.expressions import RawSQL

# make sure these are imported from your models module alongside
# InitialBorder, ContractBorder, ShrhLayer:
# from .models import Province, County


class ReportLayersMixin:
    """
    Shared report-building logic. Every method here only depends on a
    `shrh_layers` queryset, not on where it came from — so InitialBorder,
    Province and County views can all reuse it as-is.
    """

    def _build_report(self, shrh_layers) -> dict:
        return {
            "geochemistry_point": self._get_geochemistry_point_report(shrh_layers),
            "geology_and_topo": self._get_geology_topo_report(shrh_layers),
            "drilling": self._get_drilling_report(shrh_layers),
            "trench": self._get_minetrench_report(shrh_layers),
            "collar": self._get_collar_report(shrh_layers),
            "geophysic_point": self._get_geophysic_point_report(shrh_layers),
            "geology_point": self._get_geology_point_report(shrh_layers),
        }

    def _get_geochemistry_point_report(self, shrh_layers) -> dict:
        """Generate report for geochemistry point layers from contracts."""
        relevant_layers = shrh_layers.filter(
            layer_name__dtyp__code=11,
            layer_name__lyrgroup_en="Geochemistry",
            layer_name__geometrytype="point"
        ).exclude(layer_name__layername_en="Gch_Pt_Sug_Pt")

        total_count = 0
        by_layer = []

        for shrh_layer in relevant_layers:
            model = get_model_from_string(
                model_app_label=LayersConfig.name,
                model_class_name=shrh_layer.layer_name.layername_en
            )
            if model is None:
                continue

            count = model.objects.filter(shr_layer_id=shrh_layer.pk).count()
            total_count += count

            by_layer.append({
                "value": count,
                "layername_fa": shrh_layer.layer_name.layername_fa,
                "contract": shrh_layer.contractborder.contract.title,
            })

        return {
            "bylayer": by_layer,
            "message": "نمونه‌ برداری ژیوشیمی",
            "unit": "تعداد",
            "help": "همه گروه ژیوشیمی که point هستند از قراردادهای مرتبط",
            "all": total_count
        }

    def _get_geology_topo_report(self, shrh_layers) -> dict:
        """Generate report for geology and topography layers."""
        relevant_layers = shrh_layers.filter(
            layer_name__dtyp__code=11,
            layer_name__layername_en="Rck_Typ_Area_Pg",
            layer_name__geometrytype="fill"
        )

        total_area_sqkm = 0
        by_layer = []

        for shrh_layer in relevant_layers:
            model = get_model_from_string(
                model_app_label=LayersConfig.name,
                model_class_name=shrh_layer.layer_name.layername_en
            )
            if model is None:
                continue

            area_sqm = model.objects.filter(
                shr_layer_id=shrh_layer.pk
            ).aggregate(
                total=Sum(RawSQL("ST_Area(border::geography)", []))
            )['total']

            area_sqm = area_sqm or 0
            area_sqkm = area_sqm / 1_000_000
            total_area_sqkm += area_sqkm

            by_layer.append({
                "value": area_sqkm,
                "layername_fa": shrh_layer.layer_name.layername_fa,
                "geometrytype": shrh_layer.layer_name.geometrytype,
                "contract": shrh_layer.contractborder.contract.title,
            })

        return {
            "bylayer": by_layer,
            "message": "زمین شناسی",
            "unit": "کیلومتر مربع",
            "help": "لایه Rck_Typ_Area_Pg از قراردادهای مرتبط",
            "all": total_area_sqkm
        }

    def _get_drilling_report(self, shrh_layers) -> dict:
        """Generate report for drilling layers."""
        selected_layers_names = [
            "Extraction_Operation_Drilling_Pg",
            "Extraction_Operation_Drilling_Pl",
            "Extraction_Operation_Drilling_Pt"
        ]
        relevant_layers = shrh_layers.filter(
            layer_name__dtyp__code=11,
            layer_name__layername_en__in=selected_layers_names
        )

        total_depth = 0
        by_layer = []

        for shrh_layer in relevant_layers:
            model = get_model_from_string(
                model_app_label=LayersConfig.name,
                model_class_name=shrh_layer.layer_name.layername_en
            )
            if model is None:
                continue

            depth = model.objects.filter(
                shr_layer_id=shrh_layer.pk
            ).aggregate(total=Sum('depth'))['total'] or 0
            total_depth += depth

            by_layer.append({
                "value": depth,
                "layername_fa": shrh_layer.layer_name.layername_fa,
                "geometrytype": shrh_layer.layer_name.geometrytype,
                "contract": shrh_layer.contractborder.contract.title,
            })

        return {
            "bylayer": by_layer,
            "message": "میزان حفاری",
            "unit": "متر",
            "help": "مجموع فیلد depth از قراردادهای مرتبط",
            "all": total_depth
        }

    def _get_minetrench_report(self, shrh_layers) -> dict:
        """Generate report for mine trench layer."""
        selected_layers_names = ["Min_Trn_Pg", "Min_Trn_Pl", "Min_Trn_Pt"]
        relevant_layers = shrh_layers.filter(
            layer_name__dtyp__code=11,
            layer_name__layername_en__in=selected_layers_names
        )

        total_depth = 0
        by_layer = []

        for shrh_layer in relevant_layers:
            model = get_model_from_string(
                model_app_label=LayersConfig.name,
                model_class_name=shrh_layer.layer_name.layername_en
            )
            if model is None:
                continue

            depth = model.objects.filter(
                shr_layer_id=shrh_layer.pk
            ).aggregate(total=Sum('depth'))['total'] or 0
            total_depth += depth

            by_layer.append({
                "value": depth,
                "layername_fa": shrh_layer.layer_name.layername_fa,
                "geometrytype": shrh_layer.layer_name.geometrytype,
                "contract": shrh_layer.contractborder.contract.title,
            })

        return {
            "bylayer": by_layer,
            "message": "میزان ترانشه",
            "unit": "متر",
            "help": "مجموع فیلد depth از قراردادهای مرتبط",
            "all": total_depth
        }

    def _get_collar_report(self, shrh_layers) -> dict:
        """Generate report for mine collar layer."""
        selected_layers_names = ["Collar_Pt"]
        relevant_layers = shrh_layers.filter(
            layer_name__dtyp__code=11,
            layer_name__layername_en__in=selected_layers_names
        )

        total_depth = 0
        by_layer = []

        for shrh_layer in relevant_layers:
            model = get_model_from_string(
                model_app_label=LayersConfig.name,
                model_class_name=shrh_layer.layer_name.layername_en
            )
            if model is None:
                continue

            depth = model.objects.filter(
                shr_layer_id=shrh_layer.pk
            ).aggregate(total=Sum('depth'))['total'] or 0
            total_depth += depth

            by_layer.append({
                "value": depth,
                "layername_fa": shrh_layer.layer_name.layername_fa,
                "geometrytype": shrh_layer.layer_name.geometrytype,
                "contract": shrh_layer.contractborder.contract.title,
            })

        return {
            "bylayer": by_layer,
            "message": "میزان گمانه",
            "unit": "متر",
            "help": "مجموع فیلد depth از قراردادهای مرتبط",
            "all": total_depth
        }

    def _get_geophysic_point_report(self, shrh_layers) -> dict:
        """Generate report for geophysic point layers from contracts."""
        relevant_layers = shrh_layers.filter(
            layer_name__dtyp__code=11,
            layer_name__lyrgroup_en="Geophysic",
            layer_name__layername_en="Gph_P_Pt",
            layer_name__geometrytype="point"
        )

        total_count = 0
        by_layer = []

        for shrh_layer in relevant_layers:
            model = get_model_from_string(
                model_app_label=LayersConfig.name,
                model_class_name=shrh_layer.layer_name.layername_en
            )
            if model is None:
                continue

            count = model.objects.filter(shr_layer_id=shrh_layer.pk).count()
            total_count += count

            by_layer.append({
                "value": count,
                "layername_fa": shrh_layer.layer_name.layername_fa,
                "contract": shrh_layer.contractborder.contract.title,
            })

        return {
            "bylayer": by_layer,
            "message": "نمونه‌ برداری ژئوفیزیک",
            "unit": "تعداد",
            "help": "همه گروه ژئوفیزیک لایه نقاط برداشت ژئوفيزيک که point هستند از قراردادهای مرتبط",
            "all": total_count
        }

    def _get_geology_point_report(self, shrh_layers) -> dict:
        """Generate report for geology point layers from contracts."""
        relevant_layers = shrh_layers.filter(
            layer_name__dtyp__code=11,
            layer_name__lyrgroup_en="Geology",
            layer_name__layername_en="Glg_Smpl_Lc_Pt",
            layer_name__geometrytype="point"
        )

        total_count = 0
        by_layer = []

        for shrh_layer in relevant_layers:
            model = get_model_from_string(
                model_app_label=LayersConfig.name,
                model_class_name=shrh_layer.layer_name.layername_en
            )
            if model is None:
                continue

            count = model.objects.filter(shr_layer_id=shrh_layer.pk).count()
            total_count += count

            by_layer.append({
                "value": count,
                "layername_fa": shrh_layer.layer_name.layername_fa,
                "contract": shrh_layer.contractborder.contract.title,
            })

        return {
            "bylayer": by_layer,
            "message": "نمونه‌ برداری زمین شناسی",
            "unit": "تعداد",
            "help": "همه گروه زمین شناسی لایه محل نمونه برداری که point هستند از قراردادهای مرتبط",
            "all": total_count
        }

class ReportLayers(ReportLayersMixin, APIView):
    # permission is dynamic

    def get(self, request: Request, initialborderid: int) -> Response:
        try:
            initialborder_instance = InitialBorder.objects.get(pk=initialborderid)

            contract_borders = ContractBorder.objects.filter(
                initborder=initialborder_instance
            ).select_related('contract')

            shrh_layers = ShrhLayer.objects.filter(
                contractborder__in=contract_borders
            ).select_related('layer_name', 'shrh_base', 'contractborder__contract')

            result = self._build_report(shrh_layers)
            return Response(result, status=status.HTTP_200_OK)

        except InitialBorder.DoesNotExist:
            return Response(
                {"detail": "محدوده اولیه یافت نشد"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error in ReportLayers.get: {e}")
            return Response(
                {"detail": "خطا در گزارش لایه های قرارداد"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReportLayersByProvince(ReportLayersMixin, APIView):
    # permission is dynamic

    def get(self, request: Request, provinceid: int) -> Response:
        try:
            province_instance = Province.objects.get(pk=provinceid)

            # InitialBorder.province is already precomputed via spatial
            # intersection in InitialBorder.save(), so we can filter directly.
            initial_borders = InitialBorder.objects.filter(province=province_instance)

            contract_borders = ContractBorder.objects.filter(
                initborder__in=initial_borders
            ).select_related('contract')

            shrh_layers = ShrhLayer.objects.filter(
                contractborder__in=contract_borders
            ).select_related('layer_name', 'shrh_base', 'contractborder__contract')

            result = self._build_report(shrh_layers)
            return Response(result, status=status.HTTP_200_OK)

        except Province.DoesNotExist:
            return Response(
                {"detail": "استان یافت نشد"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error in ReportLayersByProvince.get: {e}")
            return Response(
                {"detail": "خطا در گزارش لایه های قرارداد"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReportLayersByCounty(ReportLayersMixin, APIView):
    # permission is dynamic

    def get(self, request: Request, countyid: int) -> Response:
        try:
            county_instance = County.objects.get(pk=countyid)

            # InitialBorder has no direct relation to County, so we match the
            # same spatial-intersects approach InitialBorder.save() uses for Province.
            initial_borders = InitialBorder.objects.filter(
                border__intersects=county_instance.border
            )

            contract_borders = ContractBorder.objects.filter(
                initborder__in=initial_borders
            ).select_related('contract')

            shrh_layers = ShrhLayer.objects.filter(
                contractborder__in=contract_borders
            ).select_related('layer_name', 'shrh_base', 'contractborder__contract')

            result = self._build_report(shrh_layers)
            return Response(result, status=status.HTTP_200_OK)

        except County.DoesNotExist:
            return Response(
                {"detail": "شهرستان یافت نشد"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error in ReportLayersByCounty.get: {e}")
            return Response(
                {"detail": "خطا در گزارش لایه های قرارداد"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )