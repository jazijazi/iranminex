import os
import shutil
import logging
from logs.utils import get_details_from_request
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.db.models import Model as DjangoModel
from layers.apps import LayersConfig

from layers.utils import get_model_from_string
from layers.apps import LayersConfig
from common.services.notification_services import NotificationFactory
from common.pagination import CustomPagination
from common.mixins import SearchMixin

from accounts.models import User

from contracts.models.models import (
    ContractDomin,
    Contract,
    ShrhBase,
    ShrhLayer
)
from layers.models.models import (
    LayersNames,
    LinkedToLayerTable,
    FeatureAttachment
)

delete_logger = logging.getLogger('delete_activity_logger')

class FeatureAttachmentListApiView(SearchMixin, APIView):
    """
        List For Feature Attachment
        GET layername and id of feature from url param
        GET The Table and search in it to Find the feature record
    """
    search_fields = ["file",]
    class FeatureAttachmentListOutputSerializer(serializers.ModelSerializer):
        class FeatureAttachmentListOutputUser(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ['username','first_name_fa','last_name_fa']
        writer = FeatureAttachmentListOutputUser()
        class Meta:
            model = FeatureAttachment
            fields = ['id','upload_date','writer','file','description']

    class FeatureAttachmentListInputSerializer(serializers.ModelSerializer):
        file = serializers.FileField(
            required=True,
            allow_null=False,
        )
        description = serializers.CharField(
            required=False,
            allow_blank=True,
            allow_null=True
        )
        def validate_file(self, value):
            # Check file size
            max_size = 300 * 1024 * 1024  # 300 MB
            if value.size > max_size:
                raise serializers.ValidationError("File size cannot exceed 300 MB.")
            return value
        class Meta:
            model = FeatureAttachment
            fields = ['file','description']

    def get(self , request:Request, shrhlyr_id:int , feature_id:int)->Response:
        try: 
            thisuser = request.user
            shrhlayer_instance : ShrhLayer = ShrhLayer.objects.get(pk=shrhlyr_id)

            if not thisuser.is_superuser and not thisuser.has_sharhlayer_access(sharhlayer=shrhlayer_instance):
                return Response({"detail":"شما به این لایه شرح خدماتی دسترسی ندارید"},status=status.HTTP_400_BAD_REQUEST)
                        
            if feature_id <= 0:
                return Response({"detail": "شناسه عارضه معتبر نیست"}, status=status.HTTP_400_BAD_REQUEST)

            layername = shrhlayer_instance.layer_name.layername_en
            model_class : DjangoModel = get_model_from_string(
                                            model_app_label=LayersConfig.name,
                                            model_class_name=layername
                                        )
            
            feature_instance = model_class.objects.get(pk=feature_id)

            all_attchments = FeatureAttachment.objects.for_object(feature_instance).all()
            serializer_data = self.FeatureAttachmentListOutputSerializer(all_attchments,many=True,context={'request':request})
            return Response(serializer_data.data,status=status.HTTP_200_OK)
            

        except ShrhLayer.DoesNotExist:
            return Response(
                {"detail": "لایه شرح خدماتی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except model_class.DoesNotExist:
            return Response(
                {"detail": "عارضه ایی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error in FeatureAttachmentListApiView: {e}")
            return Response(
                {"detail": "خطا در خواندن پیوست های عارضه"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def post(self , request:Request, shrhlyr_id:int , feature_id:int)->Response:
        try:
            thisuser = request.user

            serializer = self.FeatureAttachmentListInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"details": serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data

            shrhlayer_instance : ShrhLayer = ShrhLayer.objects.get(pk=shrhlyr_id)

            if not thisuser.is_superuser and not thisuser.has_sharhlayer_access(sharhlayer=shrhlayer_instance):
                return Response({"detail":"شما به این لایه شرح خدماتی دسترسی ندارید"},status=status.HTTP_400_BAD_REQUEST)
                        
            if feature_id <= 0:
                return Response({"detail": "شناسه عارضه معتبر نیست"}, status=status.HTTP_400_BAD_REQUEST)

            layername = shrhlayer_instance.layer_name.layername_en
            model_class : DjangoModel = get_model_from_string(
                                            model_app_label=LayersConfig.name,
                                            model_class_name=layername
                                        )
            
            feature_instance = model_class.objects.get(pk=feature_id)
            
            new_feature_attachment = FeatureAttachment.objects.create(
                writer=thisuser,
                file=validated_data['file'],
                description=validated_data.get('description'),
                linked_to_project=feature_instance, #3 fields (content_type,object_id,linked_to_project) valid with this filed
            )
            new_feature_attachment.save()

            serilize_data = self.FeatureAttachmentListOutputSerializer(new_feature_attachment,context={'request':request})
            return Response(serilize_data.data , status=status.HTTP_201_CREATED)

        except model_class.DoesNotExist:
            return Response(
                {"detail": "عارضه ایی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except ShrhLayer.DoesNotExist:
            return Response(
                {"detail": "لایه شرح خدماتی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error in FeatureAttachmentListApiView: {e}")
            return Response(
                {"detail": "خطا در ساخت پیوست عارضه"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class FeatureAttachmentDetailsApiView(APIView):
    """
        List For Feature Attachment
        GET layername and id of feature from url param
        GET The Table and search in it to Find the feature record
        GET FeatueAttachment id from url
    """
    def delete(self , request:Request, shrhlyr_id:int , feature_id:int , attach_id:int)->Response:
        try:
            thisuser = request.user
            shrhlayer_instance : ShrhLayer = ShrhLayer.objects.get(pk=shrhlyr_id)

            if not thisuser.is_superuser and not thisuser.has_sharhlayer_access(sharhlayer=shrhlayer_instance):
                return Response({"detail":"شما به این لایه شرح خدماتی دسترسی ندارید"},status=status.HTTP_400_BAD_REQUEST)
                        
            if feature_id <= 0:
                return Response({"detail": "شناسه عارضه معتبر نیست"}, status=status.HTTP_400_BAD_REQUEST)

            layername = shrhlayer_instance.layer_name.layername_en
            model_class : DjangoModel = get_model_from_string(
                                            model_app_label=LayersConfig.name,
                                            model_class_name=layername
                                        )
            
            feature_instance = model_class.objects.get(pk=feature_id)

            # attach_instance = FeatureAttachment.objects.for_object(feature_instance).get(pk=attach_id) #is wrong!
            attach_instance = FeatureAttachment.objects.get(pk=attach_id)
            attach_instance.delete()
            delete_logger.warning(f"حذف پیوست عارضه از لایه {layername} فایل {attach_instance.file.path} " , extra=get_details_from_request(request))

            return Response(status=status.HTTP_204_NO_CONTENT)

        except FeatureAttachment.DoesNotExist:
            return Response(
                {"detail": "پیوست عارضه ایی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except model_class.DoesNotExist:
            return Response(
                {"detail": "عارضه ایی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except ShrhLayer.DoesNotExist:
            return Response(
                {"detail": "لایه شرح خدماتی با این آیدی وجود ندارد"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error in FeatureAttachmentDetailsApiView: {e}")
            return Response(
                {"detail": "خطا در حذف پیوست های عارضه"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
