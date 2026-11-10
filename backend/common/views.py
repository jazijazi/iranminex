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
from common.models.districts import (
    Ostan,
    Shahrestan
)
from common.models.other import Sherkat
from common.mixins import SearchMixin

from django.db import connection
from django.core.cache import cache
import time

class OstanListApiView(APIView):
    """
        List of all Ostan in Database
    """
    permission_classes=[AllowAny]
    
    class OstanListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Ostan
            fields = ['id','title' , 'center' , 'code']

    def get(self , request:Request) -> Response:
        try:
            all_ostan = Ostan.objects.all()
            output_serializer = self.OstanListOutputSerializer(all_ostan,many=True)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن لیست استان ها"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ShahrestanListApiView(APIView):
    """
        List of all Shahrestan in Database
    """
    permission_classes=[AllowAny]
    
    class ShahrestanListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Shahrestan
            fields = ['id', 'title', 'code', 'ostan']

    def get(self , request:Request) -> Response:
        try:
            all_ostan = Shahrestan.objects.all()
            output_serializer = self.ShahrestanListOutputSerializer(all_ostan,many=True)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن لیست شهرستان ها"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       

class SherkatListApiView(SearchMixin, APIView):

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
    
    class SherkatListInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Sherkat
            fields = ['name' , 'code' , 'typ' , 'service_typ' , 'callnumber' , 'address' , 'comment']
    class SherkatListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Sherkat
            fields = ['id' , 'name' , 'code' , 'typ' , 'service_typ' , 'callnumber' , 'address' , 'comment']

    def get(self , request:Request) -> Response:
        """
            GET: List of all Sherkat`s
        """
        try:
            all_sherkat = Sherkat.objects.all()
            # Add Search query param to it
            all_sherkat = self.apply_search(all_sherkat, request)
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(all_sherkat, request)
            serializer = self.SherkatListOutputSerializer(paginated_queryset,many=True,context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن لیست شرکت‌ها"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self , request:Request) -> Response:
        """
            Create new Sherkat 
        """
        try:
            serializer = self.SherkatListInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            new_sherkat  = serializer.save()
            serialized_new_sherkat = self.SherkatListOutputSerializer(new_sherkat)
            return Response(serialized_new_sherkat.data , status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در ایجاد شرکت جدید"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        

class SherkatDetailsApiView(APIView):
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

    class SherkatDetailsOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Sherkat
            fields = ['id' , 'name' , 'code' , 'typ' , 'service_typ' , 'callnumber' , 'address' , 'comment']

    class SherkatDetailsInputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Sherkat
            fields = ['name' , 'code' , 'typ' , 'service_typ' , 'callnumber' , 'address' , 'comment']


    def get(self , request:Request, sherkatid:int) -> Response:
        try:
            sherkat_instance = Sherkat.objects.get(pk=sherkatid)
            serializer = self.SherkatDetailsOutputSerializer(sherkat_instance)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except Sherkat.DoesNotExist:
            return Response({"detail":"شرکت با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن شرکت با این آیدی"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self , request:Request, sherkatid:int) -> Response:
        try:
            sherkat_instance = Sherkat.objects.get(pk=sherkatid)
            serializer = self.SherkatDetailsInputSerializer(
                sherkat_instance, 
                data=request.data, 
                partial=True  # Allow partial updates
            )
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            updated_sherkat = serializer.save()
            serailized_updated_sherkat = self.SherkatDetailsOutputSerializer(updated_sherkat)
            return Response(serailized_updated_sherkat.data , status=status.HTTP_200_OK)
        except Sherkat.DoesNotExist:
            return Response({"detail":"شرکت با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن شرکت با این آیدی"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self , request:Request , sherkatid:str) -> Response:
        try:
            contract_instance = Sherkat.objects.get(pk=sherkatid)
            contract_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Sherkat.DoesNotExist:
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
