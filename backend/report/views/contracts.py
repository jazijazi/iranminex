import os
import uuid
from typing import cast, Dict, Any
from django.db.models import Count, Sum, Q, F, Case, When, DecimalField, ExpressionWrapper, FloatField , BigIntegerField
from django.db.models.functions import Coalesce
from django.db.models.expressions import RawSQL
from django.conf import settings
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
    ContractElhaghye,
    ContractDomin,
    ContractBorder,
    ShrhLayer,
    ShrhBase,
)
from report.services.contract_in_word import (
    create_word_form_contract_summary
)
from report.services.contract_in_excel import (
    create_excel_form_contract_summary
)
from report.services.contract_in_pdf import (
    create_pdf_form_contract_summary
)

class ReportContracts(APIView):
    # permission is dynamic

    def get(self , request:Request) -> Response:
        try:
            user = request.user

            # Single query with all aggregations on Contract
            stats = Contract.objects.aggregate(
                # Counts
                completed_count=Count('id', filter=Q(is_completed=True)),
                not_completed_count=Count('id', filter=Q(is_completed=False)),
                
                # Sum of mablagh for all
                total_mablagh=Sum('mablagh'),
                
                # Sum of mablagh for completed
                completed_mablagh=Sum('mablagh', filter=Q(is_completed=True)),
                
                # Sum of mablagh for not completed
                not_completed_mablagh=Sum('mablagh', filter=Q(is_completed=False)),
            )

            # Separate aggregation on ContractElhaghye, joined back to contract.is_completed
            elhaghye_stats = ContractElhaghye.objects.aggregate(
                total_mablaghe_elhaghye=Sum('mablagh'),
                completed_mablaghe_elhaghye=Sum('mablagh', filter=Q(contract__is_completed=True)),
                not_completed_mablaghe_elhaghye=Sum('mablagh', filter=Q(contract__is_completed=False)),
            )

            # Helper function to safely add nullable values
            def safe_sum(*values):
                return sum(v for v in values if v is not None)
            
            result = {
                "count": {
                    "is_completed": stats['completed_count'] or 0,
                    "is_not_completed": stats['not_completed_count'] or 0
                },
                "mablagh": {
                    "all": safe_sum(
                        stats['total_mablagh'], 
                        elhaghye_stats['total_mablaghe_elhaghye']
                    ),
                    "is_completed": safe_sum(
                        stats['completed_mablagh'], 
                        elhaghye_stats['completed_mablaghe_elhaghye']
                    ),
                    "is_not_completed": safe_sum(
                        stats['not_completed_mablagh'], 
                        elhaghye_stats['not_completed_mablaghe_elhaghye']
                    )
                }
            }
            
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"detail": "خطا در گزارش کلی قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ReportContractsByCompany(APIView):
    # permission is dynamic

    def get(self , request:Request) -> Response:
        try:
            user = request.user

            # First query: contract-level stats per company (mablagh only)
            company_stats = Company.objects.annotate(
                # Count completed contracts
                completed_count=Count(
                    'rcompanycontracts',
                    filter=Q(rcompanycontracts__is_completed=True),
                    distinct=True
                ),
                # Count not completed contracts
                not_completed_count=Count(
                    'rcompanycontracts',
                    filter=Q(rcompanycontracts__is_completed=False),
                    distinct=True
                ),
                # Sum all mablagh
                total_mablagh=Sum('rcompanycontracts__mablagh', distinct=True),
                
                # Sum completed mablagh
                completed_mablagh=Sum(
                    'rcompanycontracts__mablagh',
                    filter=Q(rcompanycontracts__is_completed=True),
                    distinct=True
                ),
                
                # Sum not completed mablagh
                not_completed_mablagh=Sum(
                    'rcompanycontracts__mablagh',
                    filter=Q(rcompanycontracts__is_completed=False),
                    distinct=True
                ),
            ).filter(
                Q(completed_count__gt=0) | Q(not_completed_count__gt=0)
            ).values(
                'id',
                'name',
                'typ',
                'completed_count',
                'not_completed_count',
                'total_mablagh',
                'completed_mablagh',
                'not_completed_mablagh',
            ).order_by('name')

            # Second query: elhaghye stats per company, via Company -> Contract -> ContractElhaghye
            elhaghye_stats = Company.objects.annotate(
                total_mablaghe_elhaghye=Sum('rcompanycontracts__relhaghyeha__mablagh'),
                completed_mablaghe_elhaghye=Sum(
                    'rcompanycontracts__relhaghyeha__mablagh',
                    filter=Q(rcompanycontracts__is_completed=True)
                ),
                not_completed_mablaghe_elhaghye=Sum(
                    'rcompanycontracts__relhaghyeha__mablagh',
                    filter=Q(rcompanycontracts__is_completed=False)
                ),
            ).values(
                'id',
                'total_mablaghe_elhaghye',
                'completed_mablaghe_elhaghye',
                'not_completed_mablaghe_elhaghye',
            )

            # Build a lookup dict for fast merging by company id
            elhaghye_by_company = {row['id']: row for row in elhaghye_stats}

            # Helper function to safely add nullable values
            def safe_sum(*values):
                return sum(v for v in values if v is not None)
            
            # Build result list
            result = []
            for company in company_stats:
                elhaghye = elhaghye_by_company.get(company['id'], {})
                result.append({
                    "company_name": company['name'],
                    "company_typ": company['typ'] or "",  # Handle None
                    "count": {
                        "is_completed": company['completed_count'] or 0,
                        "is_not_completed": company['not_completed_count'] or 0
                    },
                    "mablagh": {
                        "all": safe_sum(
                            company['total_mablagh'],
                            elhaghye.get('total_mablaghe_elhaghye')
                        ),
                        "is_completed": safe_sum(
                            company['completed_mablagh'],
                            elhaghye.get('completed_mablaghe_elhaghye')
                        ),
                        "is_not_completed": safe_sum(
                            company['not_completed_mablagh'],
                            elhaghye.get('not_completed_mablaghe_elhaghye')
                        )
                    }
                })
            
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"detail": "خطا در گزارش قرارداد بر اساس شرکت"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
class ReportContractsBySharh(APIView):
    # permission is dynamic

    def get(self, request: Request) -> Response:
        try:
            user = request.user

            contracts_stats = Contract.objects.annotate(
                shrh_count=Count('shrh_items'),
                total_percentage_sum=Coalesce(Sum('shrh_items__percentage'), 0),
                worked_percentage_sum=Coalesce(Sum('shrh_items__worked_percentage'), 0),
            ).filter(
                shrh_count__gt=0
            ).values(
                'id',
                'title',
                'number',
                'is_completed',
                'progress',
                'mablagh',
                'shrh_count',
                'total_percentage_sum',
                'worked_percentage_sum',
            ).order_by('title')

            # Separate query: sum of elhaghye amounts per contract
            elhaghye_stats = ContractElhaghye.objects.values('contract_id').annotate(
                total_mablaghe_elhaghye=Sum('mablagh')
            )
            elhaghye_by_contract = {
                row['contract_id']: row['total_mablaghe_elhaghye'] or 0
                for row in elhaghye_stats
            }

            result = []
            for contract in contracts_stats:
                base_mablagh = contract['mablagh'] or 0
                elhaghye_mablagh = elhaghye_by_contract.get(contract['id'], 0)
                mablagh = base_mablagh + elhaghye_mablagh

                total_percentage = contract['total_percentage_sum']
                worked_percentage = contract['worked_percentage_sum']
                remaining_percentage = max(total_percentage - worked_percentage, 0)

                # Prices derived from mablagh
                total_price = (mablagh * total_percentage) / 100
                completed_price = (mablagh * worked_percentage) / 100
                remaining_price = max(total_price - completed_price, 0)

                # Completion percentage based on percentage fields
                if total_percentage > 0:
                    completion_percentage = min(
                        (worked_percentage / total_percentage) * 100,
                        100
                    )
                else:
                    completion_percentage = 0

                # Price completion percentage
                if total_price > 0:
                    price_completion_percentage = min(
                        (completed_price / total_price) * 100,
                        100
                    )
                else:
                    price_completion_percentage = 0

                result.append({
                    "contract_id": str(contract['id']),
                    "contract_title": contract['title'],
                    "contract_number": contract['number'] or "",
                    "is_completed": contract['is_completed'],
                    "contract_progress": contract['progress'],
                    "shrh_statistics": {
                        "total_items": contract['shrh_count'],
                        "percentage": {
                            "total": total_percentage,
                            "worked": worked_percentage,
                            "remaining": remaining_percentage,
                            "completion_percentage": round(completion_percentage, 2)
                        },
                        "price": {
                            "total": int(total_price),
                            "completed": int(completed_price),
                            "remaining": int(remaining_price),
                            "completion_percentage": round(price_completion_percentage, 2)
                        }
                    }
                })

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {"detail": "خطا در گزارش قراردادها بر اساس شرح خدمات"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class ReportContractsByInitialBorder(APIView):

    # permission is dynamic

    def get(self, request: Request, initialborderid: int) -> Response:
        try:
            user = request.user

            initialborder_instance: InitialBorder = InitialBorder.objects.get(pk=initialborderid)

            # Get all ContractBorder instances related to this InitialBorder
            contract_borders = ContractBorder.objects.filter(
                initborder=initialborder_instance
            ).select_related('contract')

            # Extract unique contracts
            contracts = Contract.objects.filter(
                rcontractborders__initborder=initialborder_instance
            ).distinct().prefetch_related('company', 'dtyp', 'relhaghyeha')

            initialborder_area = InitialBorder.objects.filter(
                pk=initialborderid
            ).annotate(
                area_sqm=RawSQL("ST_Area(border::geography)", [])
            ).values_list('area_sqm', flat=True).first()
            area_sqkm = initialborder_area / 1_000_000 if initialborder_area else 0

            contracts_data = []
            for contract in contracts:
                elhaghye_items = list(contract.relhaghyeha.all())
                total_mablaghe_elhaghye = sum(
                    (item.mablagh or 0) for item in elhaghye_items
                )

                contracts_data.append({
                    'id': str(contract.id),
                    'title': contract.title,
                    'number': contract.number,
                    'start_date': contract.start_date,
                    'end_date': contract.end_date,
                    'progress': contract.progress,
                    'is_completed': contract.is_completed,
                    'department': contract.department if contract.department else '',
                    'mablagh': contract.mablagh,
                    'elhaghye': len(elhaghye_items) > 0,
                    'mablaghe_elhaghye': total_mablaghe_elhaghye,
                })

            return Response(
                {
                    "initialborder": initialborder_instance.title,
                    "initialborder_area":area_sqkm,
                    "contracts": contracts_data,
                    "count": len(contracts_data)
                },
                status=status.HTTP_200_OK
            )

        except InitialBorder.DoesNotExist:
            return Response(
                {"detail": "محدوده اولیه یافت نشد"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            print(e)
            return Response(
                {"detail": "خطا در گزارش قراردادها بر اساس محدوده اولیه"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReportContractsByDomin(APIView):
    # permission is dynamic

    def get(self, request: Request, contractdoamincode: int) -> Response:
        try:
            user = request.user

            contractdomin_instance = ContractDomin.objects.get(code=contractdoamincode)

            all_contracts_with_this_code = Contract.objects.filter(dtyp=contractdomin_instance)

            if not all_contracts_with_this_code.exists():
                return Response(
                {"detail": "هیچ قراردادی با این نوع یافت شد"}, 
                status=status.HTTP_404_NOT_FOUND
            )

            # Get all initial borders related to these contracts through ContractBorder
            initial_border_ids = ContractBorder.objects.filter(
                contract__in=all_contracts_with_this_code
            ).values_list('initborder_id', flat=True).distinct()

            all_initialborders_related_to_contracts = InitialBorder.objects.filter(
                id__in=initial_border_ids
            ).select_related('dtyp').prefetch_related('rinitcontractborders__contract')


            # Build the response data
            result = []
            for initborder in all_initialborders_related_to_contracts:
                # Get all contracts related to this initial border
                related_contracts = Contract.objects.filter(
                    rcontractborders__initborder=initborder,
                    dtyp=contractdomin_instance
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
        
class ReportContractSummary(APIView):
        
    def get(self , request : Request , contractid: str):
        try:
            user : User = request.user

            contract : Contract = Contract.objects.get(pk=contractid)
            

            if not user.is_superuser and not user.has_contract_access(contract):
                return Response({"detail": "کاربر به این قرارداد دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
        
            # relative_path = create_word_form_contract_summary(
            #     contractid = contract.pk,
            #     user = user
            # )

            # relative_path = create_excel_form_contract_summary(
            relative_path = create_pdf_form_contract_summary( 
                contractid = contract.pk,
                user = user
            )


            relative_path = relative_path.replace("\\", "/")

            file_url = request.build_absolute_uri(
                os.path.join(settings.MEDIA_URL, relative_path).replace("\\", "/")
            )
            return Response({"file_url": file_url}, status=status.HTTP_200_OK)

        except Contract.DoesNotExist:
            return Response({"detail":"قراردادی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)

        
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در تولید گزارش قرارداد"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
