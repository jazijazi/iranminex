import os
import logging
from datetime import datetime
from logs.utils import get_details_from_request
from django.core.validators import FileExtensionValidator
from django.db import transaction
from django.db.models import QuerySet , Prefetch
from django.conf import settings
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework import serializers
from rest_framework.permissions import AllowAny , IsAuthenticated

from common.pagination import CustomPagination

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse

from common.models import Province
from initialborders.models.models import(
    InitialBorder,
    InitialBorderDomin,
)
from initialborders.models.attachment import(
    InitialBorderAttachment,
    InitialBorderAttachmentDomain
)
from contracts.models.models import (
    Contract,
    ContractBorder,
    ContractDomin,
)
from common.models import Company
from accounts.models import(
    User
)
from common.mixins import SearchMixin
from common.services.gis_services import queryset_to_shapefile
from initialborders.services.gis import proccess_initialborder_zipfile
from initialborders.services.metadata import get_metadatamodel_from_initialborder , create_serializer_for_initialbordermetadata

delete_logger = logging.getLogger('delete_activity_logger')
api_activity_logger = logging.getLogger('api_activity_logger')

class InitialBorderListViews(SearchMixin , APIView):
    """
        GET initialborder`s
        if user is superuser return all 
        else return only thoes user has access to it via
        shrhlayer -> contractborder -> initialborder
    """
    # look at SearchMixin its come from there !
    search_fields = ['title' , 'province__name_fa','dtyp__title']

    class InitialBorderListOutputSerializer(serializers.ModelSerializer):
        
        class InitialBorderListProvinceSerializer(serializers.ModelSerializer):
            class Meta:
                model = Province
                fields = ['id','name_fa','cnter_name_fa','code']
        class InitialBorderListDominSerializer(serializers.ModelSerializer):
            class Meta:
                model = InitialBorderDomin
                fields = ['id' , 'title' , 'code']
        dtyp = InitialBorderListDominSerializer()
        province = InitialBorderListProvinceSerializer(many=True)
        class Meta:
            model = InitialBorder
            fields = ['id' , 'title' , 'dtyp', 'province', 'center' , 'bbox' , 'parentid' ,]

    class InitialBorderListInputSerializer(serializers.ModelSerializer):
        file = serializers.FileField(
            required=True,
            allow_null=False,
            validators=[
            FileExtensionValidator(allowed_extensions=['zip'],message="فایل محدوده حتما باید با فرمت zip باشد")
        ])
        def validate_file(self, value):
            # Check file size
            max_size = 100 * 1024 * 1024  # 100 MB
            if value.size > max_size:
                raise serializers.ValidationError("File size cannot exceed 100 MB.")
            return value
        class Meta:
            model = InitialBorder
            fields = ['title','dtyp','file','parentid']

    def get(self , request:Request) -> Response:
        """
            GET: List of all InitialBorder`s
        """
        
        try:
            user : User = request.user
            if user.is_superuser: #TODO access user change
                all_initialborder = InitialBorder.objects.all()
            else:
                all_initialborder = user.get_accessible_initialborder()

            # Add Search query param to it
            all_initialborder = self.apply_search(all_initialborder, request)
            
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(all_initialborder, request)
            serializer = self.InitialBorderListOutputSerializer(paginated_queryset,many=True,context={'request': request})
            api_activity_logger.info("خواندن همه محدوده اولیه ها" , extra=get_details_from_request(request))
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن لیست محدوده اولیه {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن محوده‌های اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self , request:Request) -> Response:
        """
            POST: get initilaBorder fild
            can not have any object-level permission check!
        """
        user : User = request.user

        serializer = self.InitialBorderListInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"details": serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data

        try:
            res , border , message =  proccess_initialborder_zipfile(validated_data['file'])
            
            if not res:
                return Response({"details": message},status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():
                new_initialborder = InitialBorder.objects.create(
                    title=validated_data['title'],
                    border=border,  # This is now a MultiPolygon object
                    dtyp=validated_data.get('dtyp'),
                    parentid=validated_data.get('parentid')
                )
                
                # grant aceess on initialborder created by it self
                user.grant_initialborder_access(initial_border=new_initialborder)

            serializer = self.InitialBorderListOutputSerializer(new_initialborder)
            api_activity_logger.info(f"ساخت موفق محدوده اولیه {new_initialborder.title}" , extra=get_details_from_request(request))
            return Response(serializer.data , status=status.HTTP_201_CREATED)

        except Exception as e:
            api_activity_logger.error(f"خطا در ساخت محدوده اولیه {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail": "خطا در ساخت محدوده اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class InitialBorderDetailViews(APIView):
    """
        GET an initialborder instance
        if user is superuser has access 
        else return only thoes check user has access to it via
        shrhlayer -> contractborder -> initialborder
    """
    class InitialBorderDetaiOutputSerializer(serializers.ModelSerializer):
        class InitialBorderDetailProvinceSerializer(serializers.ModelSerializer):
            class Meta:
                model = Province
                fields = ['id','name_fa','cnter_name_fa','code']
        class InitialBorderDetailDominSerializer(serializers.ModelSerializer):
            class Meta:
                model = InitialBorderDomin
                fields = ['id' , 'title' , 'code']
        dtyp = InitialBorderDetailDominSerializer()
        province = InitialBorderDetailProvinceSerializer(many=True)
        class Meta:
            model = InitialBorder
            fields = ['id' , 'title' , 'dtyp' , 'province' , 'center' , 'bbox' , 'parentid' ,]
    
    class InitialBorderDetaiInptputSerializer(serializers.Serializer):
        file = serializers.FileField(
            required=False,
            allow_null=True,
            validators=[
                FileExtensionValidator(
                    allowed_extensions=['zip'],
                    message="فایل محدوده حتما باید با فرمت zip باشد"
                )
            ]
        )
        title = serializers.CharField(
            max_length=250,  # Fixed: max -> max_length
            required=False,  # Fixed typo: requierd -> required
            allow_blank=False,
        )
        parentid = serializers.IntegerField(
            required=False,  # Fixed typo: requierd -> required
            allow_null=True
        )
        def validate_file(self, value):
            if not value:  # If no file is provided, just return None (it's allowed)
                return value
            # Check file size
            max_size = 100 * 1024 * 1024  # 100 MB
            if value.size > max_size:
                raise serializers.ValidationError("File size cannot exceed 100 MB.")
            return value
        

    def get(self , request:Request , pk:int) -> Response:
        """
            GET:Retrive a InitialBorder instance from pk
        """
        
        try:
            user : User = request.user
            initialborder_instance = InitialBorder.objects.get(pk=pk)
            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش برای دسترسی غیرمجاز به محدوده اولیه {initialborder_instance.title}" , extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            serializer = self.InitialBorderDetaiOutputSerializer(initialborder_instance)
            api_activity_logger.info(f"دسترسی به محدوده اولیه {initialborder_instance.title}" , extra=get_details_from_request(request))
            return Response(serializer.data , status=status.HTTP_200_OK)
        except InitialBorder.DoesNotExist:
            return Response({"detail": "محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن محدوده اولیه {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن محدوده اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self , request:Request , pk:int) -> Response:
        """
            Edit A InitialBorder instance
        """
        try:
            user : User = request.user

            #Get Initialborder Instance
            initialborder_instance = InitialBorder.objects.get(pk=pk)

            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش برای ویرایش غیرمجاز به محدوده اولیه {initialborder_instance.title}" , extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            
            # Validate input data
            serializer = self.InitialBorderDetaiInptputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data
            
            # title
            if 'title' in validated_data:
                initialborder_instance.title = validated_data['title']
            
            # parentid
            if 'parentid' in validated_data:
                if validated_data['parentid'] is not None:
                    try:
                        parent_instance = InitialBorder.objects.get(pk=validated_data['parentid'])
                        initialborder_instance.parentid = parent_instance
                    except InitialBorder.DoesNotExist:
                        return Response(
                            {"detail": "محدوده اولیه قبلی یافت نشد"}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    initialborder_instance.parentid = None

            # border
            if 'file' in validated_data and validated_data['file'] is not None:
                zipfile_obj = validated_data['file']
                success, multipolygon, error = proccess_initialborder_zipfile(zipfile_obj)
                if not success:
                    return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)
                initialborder_instance.border = multipolygon

            initialborder_instance.save()

            serializer = self.InitialBorderDetaiOutputSerializer(initialborder_instance)

            api_activity_logger.info(f"ویرایش موفق محدوده اولیه {initialborder_instance.title}" , extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)

        except InitialBorder.DoesNotExist:
            return Response({"detail": "محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            api_activity_logger.error(f"خطل در ویرایش محدوده اولیه {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail": "خطا در ویرایش محوده‌های اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self , request:Request , pk:int) -> Response:
        """
            Delete :Get a InitialBorder instance from pk & Delete it
        """
        
        try:
            user : User = request.user
            initialborder_instance = InitialBorder.objects.get(pk=pk)
            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش برای حذف غیرمجاز به محدوده اولیه {initialborder_instance.title}" , extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            initialborder_instance.delete()
            delete_logger.warning(f"حذف موفق محدوده اولیه {initialborder_instance.title}" , extra=get_details_from_request(request))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InitialBorder.DoesNotExist:
            return Response({"detail": "محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            api_activity_logger.error(f"خطا در حذف محدوده اولیه {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail": "خطا در حذف محوده‌های اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class InitialBorderDownloadExportShape(APIView):

    def post(self ,  request:Request , pk:int) -> Response:
        try:
            user : User = request.user
            initialborder_instance = InitialBorder.objects.get(pk=pk)
            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش برای دسترسی غیرمجاز به محدوده اولیه {initialborder_instance.title}" , extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            
            queryset = InitialBorder.objects.filter(pk=pk)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            zip_path = queryset_to_shapefile(
                queryset=queryset,
                geometry_field="border",
                zip_output=True,
                filename=f"initialborder_{pk}_{timestamp}",
            )

            relative_path = os.path.relpath(zip_path, settings.MEDIA_ROOT)
            download_url = request.build_absolute_uri(
                f"{settings.MEDIA_URL}{relative_path}"
            )

            api_activity_logger.info(
                f"شیپ فایل محدوده اولیه {initialborder_instance.title} با موفقیت ایجاد شد",
                extra=get_details_from_request(request),
            )

            return Response(
                {
                    "detail": "شیپ فایل با موفقیت ایجاد شد",
                    "download_url": download_url,
                },
                status=status.HTTP_200_OK,
            )

        except InitialBorder.DoesNotExist:
            return Response({"detail": "محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            api_activity_logger.error(f"خطا در دانلود شیپ فایل محدوده اولیه {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail": "خطا در دانلود شیپ فایل محدوده اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AllInitialBorderDownloadExportShape(APIView):

    def post(self ,  request:Request) -> Response:
        try:
            user : User = request.user
            all_initialborder_instances = InitialBorder.objects.all()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            zip_path = queryset_to_shapefile(
                queryset=all_initialborder_instances,
                geometry_field="border",
                zip_output=True,
                filename=f"allinitialborder_{timestamp}",
            )

            relative_path = os.path.relpath(zip_path, settings.MEDIA_ROOT)
            download_url = request.build_absolute_uri(
                f"{settings.MEDIA_URL}{relative_path}"
            )

            api_activity_logger.info(
                f"شیپ فایل همه محدوده اولیه با موفقیت ایجاد شد",
                extra=get_details_from_request(request),
            )

            return Response(
                {
                    "detail": "شیپ فایل با موفقیت ایجاد شد",
                    "download_url": download_url,
                },
                status=status.HTTP_200_OK,
            )
        
        except Exception as e:
            api_activity_logger.error(f"خطا در دانلود شیپ فایل همه محدوده اولیه {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail": "خطا در دانلود شیپ فایل همه محدوده اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InitialBorderDominListView(SearchMixin, APIView):
    permission_classes = [AllowAny]
    search_fields = ['title',]
    class InitialBorderDominListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = InitialBorderDomin
            fields = ['id' , 'title' , 'code']
    
    def get(self , request:Request) -> Response:
        try:
            all_initialborderdomins = InitialBorderDomin.objects.all()
            # Add Search query param to it
            all_initialborderdomins = self.apply_search(all_initialborderdomins, request)
            serializer = self.InitialBorderDominListOutputSerializer(all_initialborderdomins,many=True)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن محوده‌های اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InitialBorderMetadatDetailsView(APIView):
    """
        Serializer for InitialBorder Metadata are Dynamically create 
        check user has aceess to this metadata of this initialborder via
        shrhlayer -> contractborder -> initialborder 
    """

    def get(self , request:Request , initialborderpk:int)->Response:
        """
            Retrive Metadata for A InitialBorder
        """

        try:
            user : User = request.user
            #GET a initialborder
            initialborder_instance = InitialBorder.objects.get(pk=initialborderpk)
            if initialborder_instance.dtyp is None:
                return Response({"detail":"نوع محدوده مشخص نشده است"},status=status.HTTP_400_BAD_REQUEST)
            #check user access to this initialborder
            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            #Get the metadata model dynamically for this initialborder
            metadata_model = get_metadatamodel_from_initialborder(initialborderpk)
            if not metadata_model:
                return Response({"detail":"این نوع محدوده اولیه شناسنامه ندارد"},status=status.HTTP_400_BAD_REQUEST)
            # Get the acctual metadata from dynamic model 
            metadata_instance = metadata_model.objects.filter(rinitialborder=initialborder_instance)
            if not metadata_instance.exists():
                return Response({"detail": "شناسنامه محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
            metadata_instance = metadata_instance.first()
            #Create dynamic serializer class base in dynamic metadata model
            metadata_serializerclass = create_serializer_for_initialbordermetadata(model_class=metadata_model)
            #Serialize the metadata base on dynamic serializer
            serialized_metadata = metadata_serializerclass(metadata_instance)

            api_activity_logger.info(f"خواندن موفق شناسنامه محدوده اولیه {initialborder_instance.title}" , extra=get_details_from_request(request))

            return Response(serialized_metadata.data , status=status.HTTP_200_OK)
        
        except InitialBorder.DoesNotExist:
            return Response({"detail": "محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن شناسنامه محدوده اولیه {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن محوده‌های اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self , request:Request , initialborderpk:int)->Response:
        """
            Edit Metadata for A InitialBorder
        """

        try:
            user : User = request.user
            #GET a initialborder
            initialborder_instance = InitialBorder.objects.get(pk=initialborderpk)
            if initialborder_instance.dtyp is None:
                return Response({"detail":"نوع محدوده مشخص نشده است"},status=status.HTTP_400_BAD_REQUEST)
            #check user access to this initialborder
            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش غیرمحاز برای ویرایش شناسنامه محدوده اولیه {initialborder_instance.title}" , extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            #Get the metadata model dynamically for this initialborder
            metadata_model = get_metadatamodel_from_initialborder(initialborderpk)
            if not metadata_model:
                return Response({"detail":"این نوع محدوده اولیه شناسنامه ندارد"},status=status.HTTP_400_BAD_REQUEST)
            # Get the acctual metadata from dynamic model 
            metadata_instance = metadata_model.objects.filter(rinitialborder=initialborder_instance)
            if not metadata_instance.exists():
                return Response({"detail": "شناسنامه محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
            metadata_instance = metadata_instance.first()
            #Create dynamic serializer class base in dynamic metadata model
            metadata_serializerclass = create_serializer_for_initialbordermetadata(model_class=metadata_model)
            #put data into serializer
            serializer = metadata_serializerclass(metadata_instance , request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        except InitialBorder.DoesNotExist:
            return Response({"detail": "محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            api_activity_logger.error(f"خطا در ویرایش شناسنامه محدوده اولیه {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail": "خطا در ویرایش شناسنامه محدوده اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class InitialBorderAttachmentListView(SearchMixin, APIView):
    """
        GET: return all attachment of one initialborder
        POST: create new attachment for one initialborder

        - Object-level check for both Get and post
        check user has aceess to this attachment of this initialborder via
        shrhlayer -> contractborder -> initialborder 
    """
    search_fields = ["file"]

    class InitialBorderAttachmentListOuputSerializer(serializers.ModelSerializer):
        class InitialBorderAttachmentUser(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ['username' , 'first_name_fa' , 'last_name_fa']
        class InitialBorderAttachmentUserDtyp(serializers.ModelSerializer):
            class Meta:
                model = InitialBorderAttachmentDomain
                fields = ['id' , 'code' , 'name' , 'category' , 'dinitialborder']
        writer = InitialBorderAttachmentUser()
        dtyp_attach = InitialBorderAttachmentUserDtyp()
        class Meta:
            model= InitialBorderAttachment
            fields= ['id' , 'file' ,'writer' , 'upload_date' , 'writed_date' , 'dtyp_attach']

    
    class InitialBorderAttachmentListInputSerializer(serializers.Serializer):
        file = serializers.FileField(required=True,allow_null=False)
        writed_date = serializers.DateTimeField(required=False,allow_null=True)
        dtyp_attach = serializers.IntegerField(required=True,allow_null=False)

        def validate_dtyp_attach(self, value):
            try:
                dtyp_attach_instance = InitialBorderAttachmentDomain.objects.get(pk=value)
                return value
            except InitialBorderAttachmentDomain.DoesNotExist:
                raise serializers.ValidationError("نوع پیوست یافت نشد")
            

    def get(self , request:Request , initialborderpk:int)->Response:
        """
            Return All Atachment`s for An InitialBorder
        """
        try:
            user : User = request.user
            
            initialborder_instance = InitialBorder.objects.get(pk=initialborderpk)
            
            #check user access to this initialborder
            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش غیرمجاز برای خواندن پیوست محدوده اولیه {initialborder_instance.title}" , extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)

            all_initialborder_attachments = InitialBorderAttachment.objects.filter(rinitialborder=initialborder_instance)
            # Add Search query param to it
            all_initialborder_attachments = self.apply_search(all_initialborder_attachments, request)
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(all_initialborder_attachments, request)
            serializer = self.InitialBorderAttachmentListOuputSerializer(paginated_queryset,many=True,context={'request': request})
            api_activity_logger.info(f"خواندن موفق پیوست‌های محدوده اولیه {initialborder_instance.title}" , extra=get_details_from_request(request))
            return paginator.get_paginated_response(serializer.data)
            
        except InitialBorder.DoesNotExist:
            return Response({"detail": "محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن پیوست محدوده اولیه {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن پیوست های محدوده اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self , request:Request , initialborderpk:int)->Response:
        """
            Create an Atachment`s for An InitialBorder
        """
        try:
            user : User = request.user
            initialborder_instance = InitialBorder.objects.get(pk=initialborderpk)
            #check user access to this initialborder
            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                api_activity_logger.warning(f"تلاش غیرمجاز برای بارگذاری پیوست محدوده اولیه {initialborder_instance.title}" , extra=get_details_from_request(request))
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            serializer = self.InitialBorderAttachmentListInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data
            
            dtyp_attach_instance = InitialBorderAttachmentDomain.objects.get(pk=validated_data['dtyp_attach'])
            
            initialborder_attachmet = InitialBorderAttachment.objects.create(
                file=validated_data['file'],
                writed_date=validated_data.get('writed_date'),
                dtyp_attach=dtyp_attach_instance,
                writer=request.user,  # Automatically set writer to current user
                rinitialborder=initialborder_instance  # Set the related InitialBorder
            )
            serializer = self.InitialBorderAttachmentListOuputSerializer(initialborder_attachmet,context={'request': request})
            api_activity_logger.info(f"بارگذاری موفق پیوست محدوده اولیه {initialborder_instance.title}" , extra=get_details_from_request(request))

            return Response(serializer.data , status=status.HTTP_201_CREATED)
            
        except InitialBorder.DoesNotExist:
            return Response({"detail": "محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except InitialBorderAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست یافت نشد"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            api_activity_logger.error(f" خطا در بارگذاری پیوست محدوده اولیه {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail": "خطا در بارگذاری پیوست محدوده اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class InitialBorderAttachmentDetailView(APIView):
    """
        GET: return one attachment with detail of one initialborder
        DELETE: delete an attachment for one initialborder
        
        - Object-level check for both Get and post
        check user has aceess to this attachment of this initialborder via
        shrhlayer -> contractborder -> initialborder 
    """
    class InitialBorderAttachmentDetailOuputSerializer(serializers.ModelSerializer):
        class InitialBorderAttachmentUser(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ['username' , 'first_name_fa' , 'last_name_fa']
        class InitialBorderAttachmentUserDtyp(serializers.ModelSerializer):
            class Meta:
                model = InitialBorderAttachmentDomain
                fields = ['id' , 'code' , 'name' , 'category' , 'dinitialborder']
        writer = InitialBorderAttachmentUser()
        dtyp_attach = InitialBorderAttachmentUserDtyp()
        class Meta:
            model= InitialBorderAttachment
            fields= ['id' , 'file' ,'writer' , 'upload_date' , 'writed_date' , 'dtyp_attach']

    def get(self , request:Request , attachmentpk:int)->Response:
        try:
            user : User = request.user
            initialborderattachment_instance = InitialBorderAttachment.objects.get(pk=attachmentpk)
            #check user access to this initialborder
            if not user.is_superuser and not user.has_access_to_initialborder(initialborderattachment_instance.rinitialborder):
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            serializer = self.InitialBorderAttachmentDetailOuputSerializer(initialborderattachment_instance,context={"request":request})
            return Response(serializer.data , status=status.HTTP_200_OK)

        except InitialBorderAttachment.DoesNotExist:
            return Response({"detail": " پیوست محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن پیوست محدوده اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self , request:Request , attachmentpk:int)->Response:
        try:
            user : User = request.user
            initialborderattachment_instance = InitialBorderAttachment.objects.get(pk=attachmentpk)
            #check user access to this initialborder
            if not user.is_superuser and not user.has_access_to_initialborder(initialborderattachment_instance.rinitialborder):
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            initialborderattachment_instance.delete()
            delete_logger.warning(f"حذف پیوست محدوده اولیه {initialborderattachment_instance.file.path}" , extra=get_details_from_request(request))
            return Response(status=status.HTTP_204_NO_CONTENT)

        except InitialBorderAttachment.DoesNotExist:
            return Response({"detail": " پیوست محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن پیوست محدوده اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class InitialBorderContractsApiView(APIView):
    class InitialBorderContractsOutputSerializer(serializers.ModelSerializer):
        class InitialBorderContractsDtypSerializer(serializers.ModelSerializer):
            class Meta:
                model = ContractDomin
                fields = ['id','title','code']
        class InitialBorderContractsCompanySerializer(serializers.ModelSerializer):
            class Meta:
                model = Company
                fields = ['id','name','typ','service_typ','code']
        dtyp = InitialBorderContractsDtypSerializer()
        contractborders = serializers.PrimaryKeyRelatedField(many=True,read_only=True,source='rcontractborders')
        company=InitialBorderContractsCompanySerializer(many=True)
        class Meta: 
            model = Contract
            fields = ['id','title','dtyp','number','progress','company',
                    'is_completed','department','mablagh','mablaghe_elhaghye',
                    'tarikh_elhaghye','start_date','end_date','elhaghye','contractborders']
    
    def get(self , request:Request , initialborderpk:int)->Response:
        """
           Get all contracts linked to an InitialBorder through ContractBorder.
           access to InitialBorder For non-superuser users check
           filter all founded contracts base on user access for non-superuser user  
        """
        try:
            user : User = request.user
            
            initialborder_instance : InitialBorder = InitialBorder.objects.get(pk=initialborderpk)
            
            #check user access to this initialborder
            if not user.is_superuser and not user.has_access_to_initialborder(initialborder_instance):
                return Response({"detail": "کاربر به این محدوده اولیه دسترسی ندارد"},status=status.HTTP_403_FORBIDDEN)
            
            all_related_contracts: QuerySet[Contract] = Contract.objects.filter(
                rcontractborders__initborder=initialborder_instance
            ).distinct().select_related('dtyp').prefetch_related(
                'company',
                Prefetch(
                    'rcontractborders',
                    queryset=ContractBorder.objects.filter(initborder=initialborder_instance)
                )
            )

            if not user.is_superuser:
                all_related_contracts.filter(
                    id__in=user.accessible_contracts.values_list('id', flat=True)
                )

            serializer = self.InitialBorderContractsOutputSerializer(all_related_contracts,many=True)

            return Response(serializer.data , status=status.HTTP_200_OK)
            
        except InitialBorder.DoesNotExist:
            return Response({"detail": "محدوده اولیه یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن پیوست های محوده‌های اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class InitialBorderAttachmentDomainListApiView(SearchMixin,APIView):
    """
        GET: List of all initialborder attachment dtyp instances
        POST: Create a New initialborder attachment dtyp instance 
    """
    search_fields = ['code','name','category']
    class InitialBorderAttachmentDomainListOutputSeializer(serializers.ModelSerializer):
        class InitialBorderAttachmentDomainListDinitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorderDomin
                fields = ['id' , 'title' , 'code']

        dinitialborder = InitialBorderAttachmentDomainListDinitialborder()
        class Meta:
            model = InitialBorderAttachmentDomain
            fields = ['id' , 'code' , 'name' , 'category' , 'dinitialborder']

    class InitialBorderAttachmentDomainListInputSeializer(serializers.ModelSerializer):
        dinitialborder = serializers.IntegerField()
        class Meta:
            model = InitialBorderAttachmentDomain
            fields = ['code' , 'name' , 'category' , 'dinitialborder']

        def validate_dinitialborder(self, value):
            if not value:
                raise serializers.ValidationError("This field cannot be empty.")
            try:
                init_domin_instance = InitialBorderDomin.objects.get(pk=value)
                return init_domin_instance
            except InitialBorderDomin.DoesNotExist:
                raise serializers.ValidationError("نوع محدوده اولیه یافت نشد")

    def get(self , request:Request)->Response:
        try:
            all_initialborderattahmentdomains = InitialBorderAttachmentDomain.objects.all()
            # Add Search query param to it
            all_initialborderattahmentdomains = self.apply_search(all_initialborderattahmentdomains, request)
            serializer = self.InitialBorderAttachmentDomainListOutputSeializer(all_initialborderattahmentdomains,many=True)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن انواع پیوست محدوده اولیه {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن انواع پیوست محدوده اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self , request:Request)->Response:
        try:
            serializer = self.InitialBorderAttachmentDomainListInputSeializer(data=request.data)
            if not serializer.is_valid():
                print("serializer.errors" , serializer.errors)
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
            new_initialborderattachmentdomain = serializer.save()
            api_activity_logger.info(f"ساخت موفق نوع پیوست محدوده اولیه " , extra=get_details_from_request(request))
            outputserializer = self.InitialBorderAttachmentDomainListOutputSeializer(new_initialborderattachmentdomain)
            return Response(outputserializer.data , status=status.HTTP_201_CREATED)
        except Exception as e:
            api_activity_logger.error(f"خطا در ساخت نوع پیوست محدوده اولیه {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail": "خطا در ساخت نوع پیوست محدوده اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class InitialBorderAttachmentDomainDetailsApiView(APIView):
    """
        GET: retrive an instance of InitialBorderAttachmentDomain
        PUT: update an instance of InitialBorderAttachmentDomain
        DELETE: delete an instance of InitialBorderAttachmentDomain
    """
    class InitialBorderAttachmentDomainDetailsOutputSeializer(serializers.ModelSerializer):
        class InitialBorderAttachmentDomainDetailsDinitialborder(serializers.ModelSerializer):
            class Meta:
                model = InitialBorderDomin
                fields = ['id' , 'title' , 'code']

        dinitialborder = InitialBorderAttachmentDomainDetailsDinitialborder()
        class Meta:
            model = InitialBorderAttachmentDomain
            fields = ['id' , 'code' , 'name' , 'category' , 'dinitialborder']

    class InitialBorderAttachmentDomainDetailsInputSeializer(serializers.ModelSerializer):
        dinitialborder = serializers.IntegerField()
        
        def validate_dinitialborder(self, value):
            try:
                init_domin_instance = InitialBorderDomin.objects.get(pk=value)
                return init_domin_instance
            except InitialBorderDomin.DoesNotExist:
                raise serializers.ValidationError("نوع محدوده اولیه یافت نشد")
        
        class Meta:
            model = InitialBorderAttachmentDomain
            fields = ['code' , 'name' , 'category' , 'dinitialborder']

    def get(self , request:Request , attachdomainpk:int)->Response:
        try:
            initialborderattahmentdomain_instance = InitialBorderAttachmentDomain.objects.get(pk=attachdomainpk)
            serializer = self.InitialBorderAttachmentDomainDetailsOutputSeializer(initialborderattahmentdomain_instance)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except InitialBorderAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست محدوده اولیه با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن نوع پیوست محدوده اولیه {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن نوع پیوست محدوده اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self , request:Request , attachdomainpk:int)->Response:
        try:
            initialborderattahmentdomain_instance = InitialBorderAttachmentDomain.objects.get(pk=attachdomainpk)
            serializer = self.InitialBorderAttachmentDomainDetailsInputSeializer(initialborderattahmentdomain_instance, data=request.data,partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
            updated_initialborderattachmentdomain = serializer.save()
            outputserializer = self.InitialBorderAttachmentDomainDetailsOutputSeializer(updated_initialborderattachmentdomain)
            return Response(outputserializer.data , status=status.HTTP_200_OK)
        except InitialBorderAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست محدوده اولیه با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            api_activity_logger.error(f"خطا در بروزرسانی نوع پیوست محدوده اولیه {str(e)}" , extra=get_details_from_request(request))
            return Response({"detail": "خطا در بروزرسانی نوع پیوست محدوده اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self , request:Request , attachdomainpk:int)->Response:
        try:
            initialborderattahmentdomain_instance = InitialBorderAttachmentDomain.objects.get(pk=attachdomainpk)
            initialborderattahmentdomain_instance.delete()
            delete_logger.warning(f"حذف نوع پیوست محدوده اولیه {initialborderattahmentdomain_instance.name}" , extra=get_details_from_request(request))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InitialBorderAttachmentDomain.DoesNotExist:
            return Response({"detail": "نوع پیوست محدوده اولیه با این آیدی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن نوع پیوست محدوده اولیه"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

