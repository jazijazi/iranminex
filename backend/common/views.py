from django.core.validators import FileExtensionValidator
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import serializers
from rest_framework.permissions import AllowAny , IsAdminUser , IsAuthenticated
from common.pagination import CustomPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import HasDynamicPermission
from common.pagination import CustomPagination
from common.models import (
    Province,
    Company,
    County,
)
from common.mixins import SearchMixin

from django.db import connection
from django.core.cache import cache
import time

class ProvinceListApiView(APIView):
    """
        List of all Province in Database
    """
    permission_classes=[AllowAny]
    
    class ProvinceListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Province
            fields = ['id','name_fa' , 'cnter_name_fa' , 'code']

    def get(self , request:Request) -> Response:
        try:
            all_province = Province.objects.all()
            output_serializer = self.ProvinceListOutputSerializer(all_province,many=True)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن لیست استان ها"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CountyListApiView(APIView):
    """
        List of all County in Database
    """
    permission_classes=[AllowAny]
    
    class CountyListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = County
            fields = ['id','name_fa' , 'code' , 'province']

    def get(self , request:Request) -> Response:
        try:
            all_province = County.objects.all()
            output_serializer = self.CountyListOutputSerializer(all_province,many=True)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن لیست شهرستان ها"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       

class CompanyListApiView(SearchMixin, APIView):

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            # For GET requests, allow any user
            return [IsAuthenticated()]
        else:
            # For all other methods (POST, PUT, PATCH, DELETE), require admin
            return [HasDynamicPermission()]
        
    search_fields = ['name' , 'code']
    
    class CompanyListInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Company
            fields = ['name' , 'code' , 'typ' , 'service_typ' , 'callnumber' , 'address' , 'comment']
    class CompanyListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Company
            fields = ['id' , 'name' , 'code' , 'typ' , 'service_typ' , 'callnumber' , 'address' , 'comment']

    def get(self , request:Request) -> Response:
        """
            GET: List of all Company`s
        """
        try:
            all_company = Company.objects.all()
            # Add Search query param to it
            all_company = self.apply_search(all_company, request)
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(all_company, request)
            serializer = self.CompanyListOutputSerializer(paginated_queryset,many=True,context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن لیست شرکت‌ها"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self , request:Request) -> Response:
        """
            Create new Company 
        """
        try:
            serializer = self.CompanyListInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            new_company  = serializer.save()
            serialized_new_company = self.CompanyListOutputSerializer(new_company)
            return Response(serialized_new_company.data , status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ایجاد شرکت جدید"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        

class CompanyDetailsApiView(APIView):
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            # For GET requests, allow any user
            return [IsAuthenticated()]
        else:
            # For all other methods (POST, PUT, PATCH, DELETE), require admin
            return [HasDynamicPermission()]

    class CompanyDetailsOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Company
            fields = ['id' , 'name' , 'code' , 'typ' , 'service_typ' , 'callnumber' , 'address' , 'comment']

    class CompanyDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Company
            fields = ['name' , 'code' , 'typ' , 'service_typ' , 'callnumber' , 'address' , 'comment']


    def get(self , request:Request, companyid:int) -> Response:
        try:
            company_instance = Company.objects.get(pk=companyid)
            serializer = self.CompanyDetailsOutputSerializer(company_instance)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({"detail":"شرکت با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن شرکت با این آیدی"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self , request:Request, companyid:int) -> Response:
        try:
            company_instance = Company.objects.get(pk=companyid)
            serializer = self.CompanyDetailsInputSerializer(
                company_instance, 
                data=request.data, 
                partial=True  # Allow partial updates
            )
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            updated_company = serializer.save()
            serailized_updated_company = self.CompanyDetailsOutputSerializer(updated_company)
            return Response(serailized_updated_company.data , status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({"detail":"شرکت با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن شرکت با این آیدی"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self , request:Request , companyid:str) -> Response:
        try:
            contract_instance = Company.objects.get(pk=companyid)
            contract_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Company.DoesNotExist:
            return Response({"detail":"شرکت با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در حذف شرکت با این آیدی"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HealthCheck(APIView):
    """
        Just a Simple Api to Check Backend Runing !
    """
    permission_classes = []
    authentication_classes = []

    def get(self , request:Request):
        health_data = {
            "status": "healthy",
            "timestamp": time.time(),
            "service": "backend",
            "version": "1.0.0"  # You can replace with your actual version
        }
        
        # Check database connectivity
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                health_data["database"] = "connected"
        except Exception as e:
            health_data["status"] = "unhealthy"
            health_data["database"] = "disconnected"
            health_data["database_error"] = str(e)
        
        # Check cache connectivity (if using Redis/Memcached)
        try:
            cache.set("health_check", "ok", 10)
            cache_value = cache.get("health_check")
            if cache_value == "ok":
                health_data["cache"] = "connected"
            else:
                health_data["cache"] = "disconnected"
        except Exception as e:
            health_data["cache"] = "disconnected"
            health_data["cache_error"] = str(e)
        
        # Return appropriate HTTP status
        http_status = status.HTTP_200_OK if health_data["status"] == "healthy" else status.HTTP_503_SERVICE_UNAVAILABLE
        
        return Response(health_data, status=http_status)
