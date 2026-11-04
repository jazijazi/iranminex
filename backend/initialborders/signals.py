from django.db.models.signals import post_save,post_delete,post_migrate
from django.dispatch import receiver

from initialborders.models.models import InitialBorder

