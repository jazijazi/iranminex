import os
import uuid
from typing import cast, Dict, Any
from django.db.models import Count, Sum, Q, F, Case, When, DecimalField, ExpressionWrapper, FloatField , BigIntegerField
from django.db.models.functions import Coalesce
from django.db.models.expressions import RawSQL
from django.core.validators import FileExtensionValidator
from rest_framework.response import Response
from rest_framework.request import Request
from django.conf import settings
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
    ShrhBase,
)

from report.services.init_contract import create_excel_from_contract_init
from report.services.init_doc import create_excel_from_initialborder_attachments
from report.services.init_in_word import create_word_from_a_initialborder , create_word_from_initialborder_summary

class ReportInitialborderContracts(APIView):
    # permission is dynamic

    def get(self, request: Request) -> Response:
        try:
            user = request.user

            all_initialborders_related_to_contracts = InitialBorder.objects.filter(
                
            ).select_related('dtyp').prefetch_related('rinitcontractborders__contract')


            # Build the response data
            result = []
            for initborder in all_initialborders_related_to_contracts:
                # Get all contracts related to this initial border
                related_contracts = Contract.objects.filter(
                    rcontractborders__initborder=initborder,
                ).select_related('dtyp').prefetch_related('company', 'relhaghyeha').distinct()

                contracts_data = []
                for contract in related_contracts:
                    elhaghye_items = list(contract.relhaghyeha.all())
                    total_mablaghe_elhaghye = sum(
                        (item.mablagh or 0) for item in elhaghye_items
                    )

                    contracts_data.append({
                        "id": str(contract.id),
                        "title": contract.title,
                        "number": contract.number,
                        "start_date": contract.start_date,
                        "end_date": contract.end_date,
                        "progress": contract.progress,
                        "is_completed": contract.is_completed,
                        "department": contract.department,
                        "elhaghye": len(elhaghye_items) > 0,
                        "mablagh": contract.mablagh,
                        "mablaghe_elhaghye": total_mablaghe_elhaghye,
                        "elhaghye_list": [
                            {
                                "id": str(item.id),
                                "title": item.title,
                                "mablagh": item.mablagh,
                                "tarikh": item.tarikh,
                                "description": item.description,
                            }
                            for item in elhaghye_items
                        ],
                        "companies": [
                            {"id": company.id, "name": company.name if hasattr(company, 'name') else str(company)} 
                            for company in contract.company.all()
                        ]
                    })

                result.append({
                    "title": initborder.title,
                    "dtyp": {
                        "title": initborder.dtyp.title if initborder.dtyp else None,
                        "code": initborder.dtyp.code if initborder.dtyp else None
                    } if initborder.dtyp else None,
                    "contracts": contracts_data
                })

            return Response(result, status=status.HTTP_200_OK)



        except ContractDomin.DoesNotExist:
            return Response(
                {"detail": "نوع قرارداد یافت نشد"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            print(e)
            return Response(
                {"detail": "خطا در گزارش قراردادها بر اساس محدوده اولیه"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InitSummaryFileReport(APIView):

    def get(self , request:Request , initborderid:int) -> Response:
        try:
            user : User = request.user
            
            initialborder : InitialBorder = InitialBorder.objects.get(pk=initborderid)

            if not user.is_superuser and not user.has_access_to_initialborder(initialborder):
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
        
            relative_path = create_word_from_initialborder_summary(
                initialborderid=initialborder.id
            )

            relative_path = relative_path.replace("\\", "/")

            file_url = request.build_absolute_uri(
                os.path.join(settings.MEDIA_URL, relative_path).replace("\\", "/")
            )
            return Response({"file_url": file_url}, status=status.HTTP_200_OK)

        except InitialBorder.DoesNotExist:
            return Response({"detail":"محدوده اولیه ایی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)

        
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در تولید گزارش محدوده اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class InitFileReport(APIView):

    def get(self , request:Request , initborderid:int) -> Response:
        try:
            user : User = request.user
            
            initialborder : InitialBorder = InitialBorder.objects.get(pk=initborderid)

            if not user.is_superuser and not user.has_access_to_initialborder(initialborder):
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
        
            relative_path = create_word_from_a_initialborder(
                initialborderid=initialborder.id
            )

            relative_path = relative_path.replace("\\", "/")

            file_url = request.build_absolute_uri(
                os.path.join(settings.MEDIA_URL, relative_path).replace("\\", "/")
            )
            return Response({"file_url": file_url}, status=status.HTTP_200_OK)

        except InitialBorder.DoesNotExist:
            return Response({"detail":"محدوده اولیه ایی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)

        
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در تولید گزارش محدوده اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class InitContractFileReport(APIView):

    def get(self , request:Request , initborderid:int , contractid:str) -> Response:
        try:
            user : User = request.user
            
            initialborder : InitialBorder = InitialBorder.objects.get(pk=initborderid)
            contract_instance : Contract = Contract.objects.get(pk=contractid)
            
            if not user.is_superuser and not user.has_contract_access(contract_instance):
                return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)

            relative_path = create_excel_from_contract_init(
            initialborder,
            contract_instance
            )

            print(relative_path)

            relative_path = relative_path.replace("\\", "/")

            file_url = request.build_absolute_uri(
                os.path.join(settings.MEDIA_URL, relative_path).replace("\\", "/")
            )
            return Response({"file_url": file_url}, status=status.HTTP_200_OK)

        except InitialBorder.DoesNotExist:
            return Response({"detail":"محدوده اولیه ایی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)

        except Contract.DoesNotExist:
            return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در تولید گزارش قرارداد محدوده"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InitDocFileReport(APIView):

    def get(self, request: Request, initborderid: int) -> Response:
        try:
            user: User = request.user
            initialborder: InitialBorder = InitialBorder.objects.get(pk=initborderid)

            if not user.is_superuser and not user.has_access_to_initialborder(initial_border=initialborder):
                return Response(
                    {"detail": "کاربر به این محدوده اولیه دسترسی ندارد"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            relative_path = create_excel_from_initialborder_attachments(
                [initialborder],
            )

            relative_path = relative_path.replace("\\", "/")

            file_url = request.build_absolute_uri(
                os.path.join(settings.MEDIA_URL, relative_path).replace("\\", "/")
            )
            return Response({"file_url": file_url}, status=status.HTTP_200_OK)

        except InitialBorder.DoesNotExist:
            return Response(
                {"detail": "محدوده اولیه ایی با این آیدی وجود ندارد"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print(e)
            return Response(
                {"detail": "خطا در تولید گزارش قرارداد پیوست محدوده اولیه"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        