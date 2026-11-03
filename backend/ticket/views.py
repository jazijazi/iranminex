import logging
from logs.utils import get_details_from_request
from django.core.validators import FileExtensionValidator
from django.db import transaction
from django.db.models import QuerySet , Prefetch
from django.db.models import ProtectedError
from typing import cast, Dict, Any
from rest_framework.response import Response
from rest_framework.request import Request
from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework.permissions import AllowAny , IsAuthenticated
from accounts.permissions import IsAdminSuperUser
from common.mixins import SearchMixin
from common.pagination import CustomPagination
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse


from accounts.models import(
    User
)
from ticket.models import (
    Ticket,
    TicketComment
)

delete_logger = logging.getLogger('delete_activity_logger')
api_activity_logger = logging.getLogger('api_activity_logger')

class TicketListApiView(SearchMixin, APIView):
    """
        GET:
          list of all tickets are in database for superuser and only my ticket for non-superuser
        POST:
          Create new ticket instance
    """
    search_fields = ['title','number']

    class TicketListOutputSerializer(serializers.ModelSerializer):
        class TicketListOutputSerializerUser(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ['id','username','first_name_fa','last_name_fa']

        created_by = TicketListOutputSerializerUser()

        class Meta:
            model = Ticket
            fields = ['number', 'title', 'body', 'category', 'status',
                      'priority','created_by','resolved_at','file']
    
    class TicketListInputSerializer(serializers.ModelSerializer):

        category = serializers.CharField()
        priority = serializers.CharField()

        def validate_file(self, value):
            max_size_mb = 10
            max_size_bytes = max_size_mb * 1024 * 1024
            if value.size > max_size_bytes:
                raise serializers.ValidationError(
                    f"حجم فایل نباید بیشتر از {max_size_mb} مگابایت باشد"
                )
            return value

        def validate_category(self, value):
            valid_choices = Ticket.Category.choices  # [(value, label), ...]
            valid_values = [choice for choice, _ in valid_choices]
            if value not in valid_values:
                choices_display = ', '.join(f"{choice} ({label})" for choice, label in valid_choices)
                raise serializers.ValidationError(
                    f"دسته‌بندی نامعتبر است. مقادیر مجاز: {choices_display}"
                )
            return value

        def validate_priority(self, value):
            valid_choices = Ticket.Priority.choices
            valid_values = [choice for choice, _ in valid_choices]
            if value not in valid_values:
                choices_display = ', '.join(f"{choice} ({label})" for choice, label in valid_choices)
                raise serializers.ValidationError(
                    f"اولویت نامعتبر است. مقادیر مجاز: {choices_display}"
                )
            return value

        class Meta:
            model = Ticket
            fields = ['title', 'body', 'category','priority','file']

    def _filter_by_query_params(self, queryset, request):
        category = request.query_params.get('category')
        priority = request.query_params.get('priority')
        ticket_status = request.query_params.get('status')

        if category:
            queryset = queryset.filter(category=category)
        if priority:
            queryset = queryset.filter(priority=priority)
        if ticket_status:
            queryset = queryset.filter(status=ticket_status)

        return queryset
    
    def get(self, request: Request) -> Response:
        try:
            user: User = request.user
            if user.is_superuser:
                all_tickets = Ticket.objects.all()
            else:
                all_tickets = Ticket.objects.filter(created_by=user)

            all_tickets = self._filter_by_query_params(all_tickets, request)
            all_tickets = self.apply_search(all_tickets, request)

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(all_tickets, request)
            serializer = self.TicketListOutputSerializer(paginated_queryset, many=True, context={'request': request})
            api_activity_logger.info("خواندن همه تیکت ها", extra=get_details_from_request(request))
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن لیست تیکت ها {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن تیکت ها"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
             

    def post(self, request: Request) -> Response:
        user: User = request.user
        try:
            serializer = self.TicketListInputSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            new_ticket = serializer.save(created_by=user, status=Ticket.Status.OPEN)
            serializer = self.TicketListOutputSerializer(new_ticket , context={'request': request})
            api_activity_logger.info(f"ساخت موفق تیکت جدید {new_ticket.pk}", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                detail = e.message_dict
            elif hasattr(e, 'messages'):
                detail = e.messages
            else:
                detail = str(e)
            return Response({"detail": detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            api_activity_logger.error(f"خطا در ساخت تیکت جدید {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ساخت تیکت جدید"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class TicketDetailApiView(APIView):
    """
    (check ticket belong to the user (if not superuser) or not)
        GET:
          retrive a ticket instance (check ticket belong to the user or not)
        PUT:
          change a ticket instance (title,desc,..) not for change status of the ticket
        DELETE:
          only superuser can delete it 
    """
    class TicketDetailOutputSerializer(serializers.ModelSerializer):
        class TicketDetailOutputSerializerUser(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ['id', 'username', 'first_name_fa', 'last_name_fa']

        created_by = TicketDetailOutputSerializerUser()

        class Meta:
            model = Ticket
            fields = ['number', 'title', 'body', 'category', 'status',
                      'priority', 'created_by', 'resolved_at', 'file']

    class TicketDetailInputSerializer(serializers.ModelSerializer):
        category = serializers.CharField()
        priority = serializers.CharField()

        def validate_file(self, value):
            max_size_mb = 10
            max_size_bytes = max_size_mb * 1024 * 1024
            if value.size > max_size_bytes:
                raise serializers.ValidationError(
                    f"حجم فایل نباید بیشتر از {max_size_mb} مگابایت باشد"
                )
            return value

        def validate_category(self, value):
            valid_choices = Ticket.Category.choices  # [(value, label), ...]
            valid_values = [choice for choice, _ in valid_choices]
            if value not in valid_values:
                choices_display = ', '.join(f"{choice} ({label})" for choice, label in valid_choices)
                raise serializers.ValidationError(
                    f"دسته‌بندی نامعتبر است. مقادیر مجاز: {choices_display}"
                )
            return value

        def validate_priority(self, value):
            valid_choices = Ticket.Priority.choices
            valid_values = [choice for choice, _ in valid_choices]
            if value not in valid_values:
                choices_display = ', '.join(f"{choice} ({label})" for choice, label in valid_choices)
                raise serializers.ValidationError(
                    f"اولویت نامعتبر است. مقادیر مجاز: {choices_display}"
                )
            return value
        
        class Meta:
            model = Ticket
            fields = ['title', 'body','category','priority','file']

    def get(self, request: Request, pk:int) -> Response:
        try:
            user: User = request.user
            ticket_instance: Ticket = Ticket.objects.get(pk=pk)

            if not user.is_superuser and not ticket_instance.created_by_id == user.id:
                return Response({"detail": "دسترسی به این تیکت مجاز نیست"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.TicketDetailOutputSerializer(ticket_instance)
            api_activity_logger.info(f"دسترسی به تیکت {ticket_instance.pk}", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({"detail": "تیکت یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            api_activity_logger.error(f"خطا در خواندن تیکت {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در خواندن تیکت"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request: Request, pk: int) -> Response:
        try:
            user: User = request.user
            ticket_instance: Ticket = Ticket.objects.get(pk=pk)

            if not user.is_superuser and not ticket_instance.created_by_id == user.id:
                return Response({"detail": "دسترسی به این تیکت مجاز نیست"}, status=status.HTTP_403_FORBIDDEN)
            
            if not ticket_instance.is_open:
                return Response({"detail": "ویرایش تیکت پایان یافته مجاز نیست"}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = self.TicketDetailInputSerializer(
                ticket_instance,
                data=request.data,
                partial=True
            )
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            updated_ticket = serializer.save()
            serializer = self.TicketDetailOutputSerializer(updated_ticket)
            api_activity_logger.info(f"ویرایش موفق تیکت {updated_ticket.pk}", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({"detail": "تیکت یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                detail = e.message_dict
            elif hasattr(e, 'messages'):
                detail = e.messages
            else:
                detail = str(e)
            return Response({"detail": detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            api_activity_logger.error(f"خطا در ویرایش تیکت {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ویرایش تیکت"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request: Request , pk: int) -> Response:
        try:
            user: User = request.user

            if not user.is_superuser:
                return Response({"detail": "تیکت فقط توسط مدیر قابل حذف است"}, status=status.HTTP_403_FORBIDDEN)
            
            ticket_instance: Ticket = Ticket.objects.get(pk=pk)
            
            ticket_instance.delete()

            delete_logger.warning(f"حذف موفق تیکت {pk}", extra=get_details_from_request(request))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Ticket.DoesNotExist:
            return Response({"detail": "تیکت یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            api_activity_logger.error(f"خطا در حذف تیکت {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در حذف تیکت"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TicketChangeStatusApiView(APIView):
    """
        change status of the ticket by superuser
    """
    permission_classes = [IsAdminSuperUser]
    

    def put(self, request: Request, pk: int) -> Response:

        try:
            user: User = request.user
            ticket_instance: Ticket = Ticket.objects.get(pk=pk)

            new_status = request.data.get("status")

            if not new_status:
                raise ValidationError({"status": "وضعیت الزامی است"})

            if new_status not in Ticket.Status.values:
                raise ValidationError(
                    {"status": f"وضعیت نامعتبر است. مقادیر مجاز: {', '.join(Ticket.Status.values)}"}
                )

            ticket_instance.status = new_status
            ticket_instance.save(update_fields=["status", "resolved_at", "updated_at"])

            status_label = Ticket.Status(new_status).label

            return Response(
                {"detail": f"وضعیت تیکت با موفقیت به {status_label} تغییر یافت"},
                status=status.HTTP_200_OK,
            )
        except Ticket.DoesNotExist:
            return Response({"detail": "تیکت یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                detail = e.message_dict
            elif hasattr(e, 'messages'):
                detail = e.messages
            else:
                detail = str(e)
            return Response({"detail": detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            api_activity_logger.error(f"خطا در ویرایش وضعیت تیکت {str(e)}", extra=get_details_from_request(request))
            return Response({"detail": "خطا در ویرایش وضعیت تیکت"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class TicketCommentListApiView(APIView):
    """
        GET:
            get all ticket comments for a ticket
        POST:
            create new ticket comment for a ticket
    """
    class TicketCommentListOutputSerializer(serializers.ModelSerializer):
        class TicketCommentListOutputSerializerUser(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ['id','username','first_name_fa','last_name_fa']

        author = TicketCommentListOutputSerializerUser()

        class Meta:
            model = TicketComment
            fields = ['id','ticket','parent','author','body','file']

    class TicketCommentListInputSerializer(serializers.ModelSerializer):
        
        def validate_file(self, value):
            max_size_mb = 10
            max_size_bytes = max_size_mb * 1024 * 1024
            if value.size > max_size_bytes:
                raise serializers.ValidationError(
                    f"حجم فایل نباید بیشتر از {max_size_mb} مگابایت باشد"
                )
            return value
        
        class Meta:
            model = TicketComment
            fields = ['body','file','parent']

    def get(self , request:Request , ticketid:int) -> Response:
        try:
            user : User = request.user

            ticket_instance : Ticket = Ticket.objects.get(pk=ticketid)

            all_ticket_comments = TicketComment.objects.filter(ticket = ticket_instance)

            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(all_ticket_comments, request)
            serializer = self.TicketCommentListOutputSerializer(paginated_queryset, many=True, context={'request': request})
            api_activity_logger.info(f"خواندن جواب تیکت های {ticket_instance.number}", extra=get_details_from_request(request))
            return paginator.get_paginated_response(serializer.data)

        except Ticket.DoesNotExist:
            return Response(
                {"detail": "تیکت یافت نشد"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            api_activity_logger.error(
                f"خطا در خواندن جواب تیکت های {ticketid} {str(e)}",
                extra=get_details_from_request(request),
            )
            return Response(
                {"detail": f"خطا در خواندن جواب تیکت های {ticketid}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self , request:Request , ticketid:int) -> Response:
        try:
            user : User = request.user

            ticket_instance : Ticket = Ticket.objects.get(pk=ticketid)

            if ticket_instance.status == Ticket.Status.CLOSED:
                return Response(
                    {"detail": "امکان ثبت پاسخ برای تیکت بسته شده وجود ندارد"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = self.TicketCommentListInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            parent = serializer.validated_data.get('parent')
            if parent and parent.ticket_id != ticket_instance.pk:
                return Response(
                    {"detail": "کامنت والد متعلق به این تیکت نیست"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            new_ticket_comment = serializer.save(ticket= ticket_instance, author=user)
            output_serializer = self.TicketCommentListOutputSerializer(new_ticket_comment, context={'request': request})
            api_activity_logger.info(f"ساخت موفق جواب تیکت جدید {new_ticket_comment.pk}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except Ticket.DoesNotExist:
            return Response(
                {"detail": "تیکت یافت نشد"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            api_activity_logger.error(
                f"خطا در ساخت جواب تیکت  {ticketid} {str(e)}",
                extra=get_details_from_request(request),
            )
            return Response(
                {"detail": f"خطا در ساخت جواب تیکت  {ticketid}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TicketCommentDetailApiView(APIView):
    """
        GET:
            retrive a ticket comment instance
        PUT:
            update a ticket comment
        Delete:
            delete a ticket comment
    """
    class TicketCommentDetaiOutpuSerializer(serializers.ModelSerializer):
        class TicketCommentDetaiOutpuSerializerUser(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ['id', 'username', 'first_name_fa', 'last_name_fa']

        author = TicketCommentDetaiOutpuSerializerUser()

        class Meta:
            model = TicketComment
            fields = ['id', 'ticket','parent' ,'author', 'body', 'file']

    class TicketCommentDetaiInputSerializer(serializers.ModelSerializer):
        def validate_file(self, value):
            max_size_mb = 10
            max_size_bytes = max_size_mb * 1024 * 1024
            if value.size > max_size_bytes:
                raise serializers.ValidationError(
                    f"حجم فایل نباید بیشتر از {max_size_mb} مگابایت باشد"
                )
            return value

        class Meta:
            model = TicketComment
            fields = ['body', 'file']

    def get(self, request: Request, pk: int) -> Response:
        try:
            user: User = request.user
            ticket_comment_instance: TicketComment = TicketComment.objects.get(pk=pk)
            serializer = self.TicketCommentDetaiOutpuSerializer(ticket_comment_instance, context={'request': request})
            api_activity_logger.info(f"خواندن جواب تیکت {ticket_comment_instance.pk}", extra=get_details_from_request(request))
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TicketComment.DoesNotExist:
            return Response(
                {"detail": "جواب تیکت یافت نشد"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            api_activity_logger.error(
                f"خطا در خواندن جواب تیکت {pk} {str(e)}",
                extra=get_details_from_request(request),
            )
            return Response(
                {"detail": f"خطا در خواندن جواب تیکت {pk}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request: Request, pk: int) -> Response:
        try:
            user: User = request.user
            ticket_comment_instance: TicketComment = TicketComment.objects.get(pk=pk)

            if not user.is_superuser and ticket_comment_instance.author_id != user.pk:
                return Response(
                    {"detail": "شما اجازه ویرایش این جواب تیکت را ندارید"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            
            serializer = self.TicketCommentDetaiInputSerializer(ticket_comment_instance, data=request.data)
            if not serializer.is_valid():
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            updated_ticket_comment = serializer.save()
            output_serializer = self.TicketCommentDetaiOutpuSerializer(updated_ticket_comment, context={'request': request})
            api_activity_logger.info(f"ویرایش موفق جواب تیکت {updated_ticket_comment.pk}", extra=get_details_from_request(request))
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        except TicketComment.DoesNotExist:
            return Response(
                {"detail": "جواب تیکت یافت نشد"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            api_activity_logger.error(
                f"خطا در ویرایش جواب تیکت {pk} {str(e)}",
                extra=get_details_from_request(request),
            )
            return Response(
                {"detail": f"خطا در ویرایش جواب تیکت {pk}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request: Request, pk: int) -> Response:
        try:
            user: User = request.user
            ticket_comment_instance: TicketComment = TicketComment.objects.get(pk=pk)

            if not user.is_superuser and ticket_comment_instance.author_id != user.pk:
                return Response(
                    {"detail": "شما اجازه حذف این جواب تیکت را ندارید"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            ticket_comment_instance.delete()
            api_activity_logger.info(f"حذف موفق جواب تیکت {pk}", extra=get_details_from_request(request))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TicketComment.DoesNotExist:
            return Response(
                {"detail": "جواب تیکت یافت نشد"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            api_activity_logger.error(
                f"خطا در حذف جواب تیکت {pk} {str(e)}",
                extra=get_details_from_request(request),
            )
            return Response(
                {"detail": f"خطا در حذف جواب تیکت {pk}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )