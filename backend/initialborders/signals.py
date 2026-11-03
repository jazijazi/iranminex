from django.db.models.signals import post_save,post_delete,post_migrate
from django.dispatch import receiver

from initialborders.models.models import InitialBorder

from initialborders.services.metadata import get_metadatamodel_from_initialborder

@receiver(post_save, sender=InitialBorder)
def create_initalborder_shenasnameh(sender, instance, created, **kwargs):
    if created:
        initialborderShenasnameh_model = get_metadatamodel_from_initialborder(instance.id)
        if initialborderShenasnameh_model:
            initialborderShenasnameh_model.objects.create(rinitialborder=instance)