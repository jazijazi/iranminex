from django.core.cache import cache
from django.db.models.signals import post_save, post_delete , m2m_changed
from django.dispatch import receiver
from django.db import transaction
from django.contrib.auth import get_user_model

from contracts.models.models import ShrhLayer
from contracts.models.comments import Comment
from common.services.notification_services import NotificationFactory

@receiver(post_save, sender=Comment)
def send_comment_notifications(sender, instance, created, **kwargs):
    if created:
        try:
            if instance.parent is not None:
                NotificationFactory.for_reply(reply=instance)
            else:
                NotificationFactory.for_comment(comment=instance)
        except Exception as e:
            print(e)