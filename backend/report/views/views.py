import uuid
from typing import cast, Dict, Any
from django.db.models import Count, Q
from django.core.validators import FileExtensionValidator
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
from django.contrib.gis.geos import MultiPolygon
from common.models import Company , Province
from accounts.models import User


from initialborders.models.models import (
    InitialBorder,
    InitialBorderDomin,
)
from contracts.models.models import (
    Contract,
    ContractDomin,
    ContractBorder,
    ShrhLayer,
)


class ReportMain(APIView):
    # permission is dynamic


    def get(self , request:Request) -> Response:
        try:
            user = request.user
            
            # Single query for InitialBorder counts grouped by domain
            initialborder_counts = InitialBorder.objects.values(
                'dtyp__title'
            ).annotate(
                count=Count('id')
            ).order_by('dtyp__title')
            
            # Build initialborder result
            initialborder_result = {
                "all": InitialBorder.objects.count()
            }
            
            for item in initialborder_counts:
                domain_title = item['dtyp__title']
                if domain_title:  # Handle null domains
                    initialborder_result[domain_title] = item['count']
            
            # Single query for Contract counts grouped by domain
            contract_counts = Contract.objects.values(
                'dtyp__title'
            ).annotate(
                count=Count('id')
            ).order_by('dtyp__title')
            
            # Build contract result
            contract_result = {
                "all": Contract.objects.count()
            }
            
            for item in contract_counts:
                domain_title = item['dtyp__title']
                if domain_title:  # Handle null domains
                    contract_result[domain_title] = item['count']
            
            # Single query for ContractBorder count
            contractborder_count = ContractBorder.objects.count()

            shrhlayer_count = ShrhLayer.objects.filter(is_uploaded=True).count()
            
            result = {
                "initialborder": initialborder_result,
                "contract": contract_result,
                "contractborder": {
                    "all": contractborder_count
                },
                "layers":{
                    "all": shrhlayer_count,
                }
            }
            
            return Response(result, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در گزارش تعداد کلی"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ReportMainByOstan(APIView):
    # permission is dynamic

    def get(self, request: Request, provinceid: int) -> Response:
        try:
            user = request.user

            province = Province.objects.get(pk=provinceid)

            # Querysets filtered by province
            initialborders = InitialBorder.objects.filter(province=province)
            contractborders = ContractBorder.objects.filter(initborder__province=province)
            contracts = Contract.objects.filter(
                id__in=contractborders.values("contract_id")
            )

            # InitialBorder counts grouped by domain
            initialborder_counts = initialborders.values(
                'dtyp__title'
            ).annotate(
                count=Count('id')
            ).order_by('dtyp__title')

            initialborder_result = {
                "all": initialborders.count()
            }
            for item in initialborder_counts:
                domain_title = item['dtyp__title']
                if domain_title:  # Handle null domains
                    initialborder_result[domain_title] = item['count']

            # Contract counts grouped by domain
            contract_counts = contracts.values(
                'dtyp__title'
            ).annotate(
                count=Count('id')
            ).order_by('dtyp__title')

            contract_result = {
                "all": contracts.count()
            }
            for item in contract_counts:
                domain_title = item['dtyp__title']
                if domain_title:  # Handle null domains
                    contract_result[domain_title] = item['count']

            # ContractBorder count
            contractborder_count = contractborders.count()

            # Uploaded layers in this province
            shrhlayer_count = ShrhLayer.objects.filter(
                contractborder__initborder__province=province,
                is_uploaded=True,
            ).count()

            result = {
                "initialborder": initialborder_result,
                "contract": contract_result,
                "contractborder": {
                    "all": contractborder_count
                },
                "layers": {
                    "all": shrhlayer_count,
                }
            }
            return Response(result, status=status.HTTP_200_OK)

        except Province.DoesNotExist:
            return Response({"detail": "استان یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در گزارش تعداد کلی برای استان"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        