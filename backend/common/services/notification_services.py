from django.contrib.contenttypes.models import ContentType
from typing import List, Optional, Union
from django.contrib.auth import get_user_model

from accounts.models import (
    User,
    Notification
)
from contracts.models.comments import (
    Comment,
)
from contracts.models.SharhKhadamats import (
    ShrhLayer,
)


class NotificationFactory:
    """
    Factory class for creating different types of notifications    
    """
    @classmethod
    def for_welcome_an_user_from_system(cls , targetuser:User) -> Notification:
        """
            Create a Function For An User 
            With No Sender Just System send it
        """

        new_notif = Notification(
            sender=None,
            receiver=targetuser,
            subject=f"پیام خوش آمد",
            text=cls._truncate_text(
                f"کاربر {cls._get_user_display_name(targetuser)} به سامانه اضافه شد",
            ),
        )

        new_notif.save()
        return new_notif
    
    @classmethod
    def for_everytime_user_login(cls , targetuser:User) -> Notification:
        """
            Create notification when a user login into system
        """

        new_notif = Notification(
            sender=None,
            receiver=targetuser,
            subject=f"ورود به حساب کاربری",
            text=cls._truncate_text(
                f"کاربر {cls._get_user_display_name(targetuser)} ورود جدیدی به حساب کاربری شما ثبت شد",
            ),
        )

        new_notif.save()
        return new_notif

    @classmethod
    def for_comment(cls, comment:Comment, exclude_users: list|None = None) -> List[Notification]:
        """
        Create notifications when a new comment is posted
        
        Args:
            comment: Comment instance
            exclude_users: List of users to exclude from notifications
            
        Returns:
            List of created notification instances
        """
        notifications = []
        exclude_users = exclude_users or []

        if not comment:
            return []
        
        # Safely get related objects
        sharh_layer = getattr(comment, 'sharhlayer', None)
        writer = getattr(comment, 'writer', None)

        # If there is no layer attached, we cannot determine who to notify.
        # Returning early prevents the crash.
        if not sharh_layer:
            return []
        
        contract_ctx = cls._get_contract_context_from_sharhlyr(sharh_layer)
        layer_name_fa = cls._get_layer_name_from_sharhlyr(sharh_layer)
        
        if writer:
            writer_name = cls._get_user_display_name(writer)
            writer_id = writer.id
        else:
            writer_name = "کاربر ناشناس"
            writer_id = -1  # Impossible ID to prevent filtering errors

        subject_text = f"نظر جدید"
        body_text = cls._truncate_text(
            f"کاربر {writer_name} در قرارداد «{contract_ctx['contract_title']}» "
            f"(شماره {contract_ctx['contract_number']})، "
            f"محدوده «{contract_ctx['contractborder_title']}»، "
            f"لایه «{layer_name_fa}» نظر جدیدی ثبت کرد"
        )

        eligible_users = sharh_layer.accessible_by_users.all()

        # Exclude the writer if they exist
        if writer_id != -1:
            eligible_users = eligible_users.exclude(id=writer_id)
        
        # Exclude additional users
        if exclude_users:
            exclude_ids = [user.id if hasattr(user, 'id') else user for user in exclude_users]
            eligible_users = eligible_users.exclude(id__in=exclude_ids)


        notifications_to_create = [
            Notification(
                sender=writer,
                receiver=user,
                subject=subject_text,
                text=body_text,
            )
            for user in eligible_users
        ]
        
        if notifications_to_create:
            notifications = Notification.objects.bulk_create(notifications_to_create)
        
        return notifications
    
    @classmethod
    def for_reply(cls, reply:Comment) -> List[Notification]:
        """
        Create notifications when someone replies to a comment
        
        Args:
            reply: Comment instance that is a reply
            
        Returns:
            List of created notification instances
        """
        notifications = []

        sharh_layer = getattr(reply, 'sharhlayer', None)
        contract_ctx = cls._get_contract_context_from_sharhlyr(sharh_layer)

        body = cls._truncate_text(
            f"{cls._get_user_display_name(reply.writer)} در قرارداد «{contract_ctx['contract_title']}» "
            f"(شماره {contract_ctx['contract_number']})، "
            f"محدوده «{contract_ctx['contractborder_title']}» به نظر شما پاسخ داد"
        ),

        if not reply.parent:
            return notifications  # Not a reply
        
        # Notify the original comment writer (if different from reply writer)
        if reply.parent.writer != reply.writer:
            notification = Notification.objects.create(
            sender=reply.writer,
            receiver=reply.parent.writer,
            subject="پاسخ به نظر شما",
            text=body
            )
            notifications.append(notification)
        
        return notifications
    
    @classmethod
    def for_layer_upload(cls , sharhlayer:ShrhLayer, uploader_user: User, exclude_users: list|None = None) -> List[Notification]:
        """
        Create notifications when a Layer Uploaded
        
        Args:
            sharhlayer: ShrhLayer instance
            exclude_users: List of users to exclude from notifications
            
        Returns:
            List of created notification instances
        """
        notifications = []
        exclude_users = exclude_users or []
        
        # 1. OPTIMIZATION: Prepare data ONCE before the loop
        try:
            # Use getattr with defaults to be safe
            layer_name_obj = getattr(sharhlayer, 'layer_name', None)
            
            layer_name_fa = getattr(layer_name_obj, 'layername_fa', 'نامشخص')
            layer_name_en = getattr(layer_name_obj, 'layername_en', 'Unknown')
            layer_group_fa = getattr(layer_name_obj, 'lyrgroup_fa', 'نامشخص')
            
            # Access contract safely
            shrh_base = getattr(sharhlayer, 'shrh_base', None)
            contract = getattr(shrh_base, 'contract', None)
            contract_title = getattr(contract, 'title', 'نامشخص')
            
            notification_text = (
                f"{cls._get_user_display_name(uploader_user)} لایه {layer_name_fa} "
                f"({layer_name_en}) برای گروه لایه {layer_group_fa} "
                f"در قرارداد {contract_title} با موفقیت بارگذاری کرد"
            )
            notification_subject = f"بارگذاری لایه جدید"

        except AttributeError:
            # Fallback text
            notification_text = (
                f"{cls._get_user_display_name(uploader_user)} لایه‌ای جدید "
                f"در {sharhlayer} بارگذاری کرد"
            )
            notification_subject = "بارگذاری لایه جدید"

        # 2. Database Query
        eligible_users = sharhlayer.accessible_by_users.exclude(id=uploader_user.id)
        
        if exclude_users:
            exclude_ids = [user.id if hasattr(user, 'id') else user for user in exclude_users]
            eligible_users = eligible_users.exclude(id__in=exclude_ids)
        
        # 3. Create Objects (Very fast now because text is pre-calculated)
        notifications_to_create = [
            Notification(
                sender=uploader_user,
                receiver=user,
                subject=notification_subject, 
                text=cls._truncate_text(notification_text),
            )
            for user in eligible_users
        ]
        
        if notifications_to_create:
            notifications = Notification.objects.bulk_create(notifications_to_create)
        
        return notifications
    
    @staticmethod
    def _get_contract_context_from_sharhlyr(sharh_layer: ShrhLayer | None) -> dict:
        """
        Safely extract contract title, contract number, and border title
        from a ShrhLayer instance.
        """

        defaults = {
            "contract_title": "نامشخص",
            "contract_number": "نامشخص",
            "contractborder_title": "نامشخص",
        }

        if not sharh_layer:
            return defaults

        try:
            shrh_base = getattr(sharh_layer, 'shrh_base', None)
            contract = getattr(shrh_base, 'contract', None)
            contractborder = getattr(sharh_layer, 'contractborder', None)

            return {
                "contract_title": getattr(contract, 'title', 'نامشخص') or 'نامشخص',
                "contract_number": getattr(contract, 'number', 'نامشخص') or 'نامشخص',
                "contractborder_title": getattr(contractborder, 'title', 'نامشخص') or 'نامشخص',
            }
        except Exception:
            return defaults

    @staticmethod
    def _get_layer_name_from_sharhlyr(sharh_layer: ShrhLayer | None) -> str:
        """
        Safely extract the Persian layer name from a ShrhLayer instance.
        """
        if not sharh_layer:
            return "نامشخص"

        try:
            layer_name_obj = getattr(sharh_layer, 'layer_name', None)
            return getattr(layer_name_obj, 'layername_fa', 'نامشخص') or 'نامشخص'
        except Exception:
            return "نامشخص"
    @staticmethod
    def _get_user_display_name(user) -> str:
        """Get the best display name for a user"""
        if user.first_name_fa and user.last_name_fa:
            return f"{user.first_name_fa} {user.last_name_fa}"
        elif user.first_name and user.last_name:
            return f"{user.first_name} {user.last_name}"
        else:
            return user.username
    
    @staticmethod
    def _truncate_text(text: str, max_length: int = 1999) -> str:
        """Truncate text to specified length"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."