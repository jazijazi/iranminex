# signals.py - Simple synchronous version without Celery
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete , m2m_changed
from django.dispatch import receiver
from django.db import transaction
from django.contrib.auth import get_user_model

from .models import (
    UserShrhLayerPermission,
    Apis,
    Roles,
    User,
)

from common.services.notification_services import NotificationFactory


User = get_user_model()

def invalidate_role_cache(role: Roles) -> None:
    users = User.objects.filter(roles=role)
    for user in users:
        cache_key = f"user:{user.id}:role:{role.id}:allowed_apis"
        cache.delete(cache_key)

# 1. When APIs are added/removed from Roles
@receiver(m2m_changed, sender=Roles.apis.through)
def clear_cache_on_role_api_change(sender, instance: Roles, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        invalidate_role_cache(instance)

# 2. When a Role is updated or deleted
@receiver([post_save, post_delete], sender=Roles)
def clear_cache_on_role_update(sender, instance: Roles, **kwargs):
    invalidate_role_cache(instance)

# 3. When an API is updated or deleted — must find related Roles
@receiver([post_save, post_delete], sender=Apis)
def clear_cache_on_api_update(sender, instance: Apis, **kwargs):
        roles = instance.rrolesapis.all()  # reverse relation from Apis to Roles
        for role in roles:
            invalidate_role_cache(role)


#NOTIFICATION
@receiver(post_save, sender=User)
def welcome_notification(sender, instance, created, **kwargs):
    """
    When A User Created 
    -> update user's accessible contracts
    """
    if created:
        NotificationFactory.for_welcome_an_user_from_system(targetuser=instance)


