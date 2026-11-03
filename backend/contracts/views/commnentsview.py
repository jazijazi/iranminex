import logging
from logs.utils import get_details_from_request
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

from accounts.models import User

from accounts.permissions import (
    HasDynamicPermission,
    HasShrhLayerAccess,
)

from contracts.models.models import (
    Contract,
)
from contracts.models.SharhKhadamats import (
    ShrhLayer,
)
from contracts.models.comments import (
    Comment,
)

delete_logger = logging.getLogger('delete_activity_logger')


class CommentListApiView(APIView):
    """
        Comments are related to sharhLayer instance
        (Get sharhlayer id from url param)
    """
    permission_classes = [HasDynamicPermission , HasShrhLayerAccess]

    class CommentListOutputSerializer(serializers.ModelSerializer):
        class CommentListOutputSerializerUser(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ['username','first_name_fa','last_name_fa']

        writer = CommentListOutputSerializerUser()

        class Meta:
            model = Comment
            fields = ['pk','writer','parent','text','created_at']

    class CommentListInputSerializer(serializers.ModelSerializer):
        parent_id = serializers.IntegerField(required=False)
        class Meta:
            model = Comment
            fields = ['parent_id' , 'text']

        def validate_parent_id(self, value):
            """Validate parent comment exists and belongs to the same sharhlayer"""
            if value is not None:
                print("validate_parent >>>>>" , value)
                try:
                    parent_comment = Comment.objects.get(pk=value)
                    return value
                except Comment.DoesNotExist:
                    raise serializers.ValidationError("نظر والد با این آیدی وجود ندارد")
            return None
            
        def validate_text(self, value):
            if not value or not value.strip():
                raise serializers.ValidationError("متن نظر نمی‌تواند خالی باشد")
            return value.strip()

    def get(self , request:Request , shrhlayerid:int) -> Response:
        """
            Return List of All Comment related to this sharhlayer instance
        """
        try:
            thisuser = request.user
            shrhlayer_instance = ShrhLayer.objects.get(pk=shrhlayerid) 
                        
            all_comments = Comment.objects.filter(sharhlayer=shrhlayer_instance).order_by('-created_at')
            serializ_data = self.CommentListOutputSerializer(all_comments , many=True)
            return Response(serializ_data.data , status=status.HTTP_200_OK)

        except ShrhLayer.DoesNotExist:
            return Response({"detail":"لایه شرح خدماتی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن نظرات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self , request:Request , shrhlayerid:int) -> Response:
        """
            Create A New Comment to the SharhLayer Instance
        """
        try:

            thisuser = request.user
            shrhlayer_instance = ShrhLayer.objects.get(pk=shrhlayerid) 
                        
            # Check if user's last comment on this sharhlayer
            last_comment = Comment.objects.filter(
                sharhlayer=shrhlayer_instance
            ).order_by('-created_at').first()
            
            # No need this condition any more
            # if last_comment and last_comment.writer == thisuser:
            #     return Response(
            #         {"detail": "شما نمی‌توانید پشت سر هم نظر بگذارید. منتظر پاسخ دیگر کاربران باشید"}, 
            #         status=status.HTTP_400_BAD_REQUEST
            #     )
            
            serializer = self.CommentListInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Get validated data
            validated_data = serializer.validated_data
            parent_id = validated_data.get('parent_id')
            text = validated_data.get('text')

            # Additional validation: if parent exists, ensure it belongs to the same sharhlayer
            parent_comment = None
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(pk=parent_id)
                    if parent_comment.sharhlayer != shrhlayer_instance:
                        return Response(
                            {"detail": "نظر والد متعلق به این لایه شرح خدماتی نیست"}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except Comment.DoesNotExist:
                    return Response(
                        {"detail": "نظر والد وجود ندارد"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            new_comment = Comment.objects.create(
                sharhlayer=shrhlayer_instance,
                writer=thisuser,
                parent=parent_comment,
                text=text
            )

            output_serializer = self.CommentListOutputSerializer(new_comment)
            return Response(output_serializer.data,status=status.HTTP_201_CREATED)

        except ShrhLayer.DoesNotExist:
            return Response({"detail":"لایه شرح خدماتی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"detail": "خطا در خواندن نظرات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# class CommentDetailsApiView(APIView):

#     permission_classes = [HasDynamicPermission , HasShrhLayerAccess]

#     def delete(self , request:Request , shrhlayerid:int , commentid:int) -> Response:
#         """
#             Delete A Comment buy user 
#         """
#         try:
#             thisuser = request.user
#             shrhlayer_instance = ShrhLayer.objects.get(pk=shrhlayerid) 
                        
#             comment_instance = Comment.objects.get(pk=commentid)

#             if not (thisuser == comment_instance.writer or thisuser.is_superuser):
#                 return Response({"detail":"شما اجازه حذف این نظر را ندارید"},status=status.HTTP_400_BAD_REQUEST)
            
#             comment_instance.delete()
#             delete_logger.warning(f"حذف یک نظر {comment_instance.writer.username}" , extra=get_details_from_request(request))

#             return Response(status=status.HTTP_204_NO_CONTENT)
        
#         except Comment.DoesNotExist:
#             return Response({"detail":"نظری با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
#         except ShrhLayer.DoesNotExist:
#             return Response({"detail":"لایه شرح خدماتی با این آیدی وجود ندارد"},status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             print(e)
#             return Response({"detail": "خطا در خواندن نظرات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)