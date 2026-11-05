from django.db import models
from django.contrib.gis.db import models as gis_models

from common.models import CustomModel , Province
from contracts.models.models import Contract

class InitialBorderDomin(CustomModel):
    title = models.CharField(max_length=100, unique=True)
    code = models.IntegerField(unique=True)
    
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "نوع محدوده اولیه"
        verbose_name_plural = "انواع محدوده اولیه"

class InitialBorder(CustomModel):
    title = models.CharField(
        max_length=250,
        unique=False,
        blank=False,
        null=False,
    )
    # Many initial borders -> one contract.
    # null/blank=True because an initial border can be created separately,
    # before it is attached to any contract.
    contract = models.ForeignKey(
        Contract,
        verbose_name="قرارداد",
        on_delete=models.SET_NULL,
        related_name="initborders",
        blank=True,
        null=True,
    )
    dtyp = models.ForeignKey(
        InitialBorderDomin,
        on_delete=models.SET_NULL,
        related_name="rinitialborderdomin",
        blank=True,
        null=True,
    )
    parentid = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name="rparentinitialborder",
        blank=True,
        null=True,
    )
    border = gis_models.MultiPolygonField(
        srid=4326,
        blank=False,
        null=False,
    )
    province = models.ManyToManyField(
        Province,
        verbose_name="استان",
        related_name="rprovinceinitialborder",
        blank=True,
    )
 
    @property
    def center(self):
        centroid = self.border.centroid
        return [centroid.x, centroid.y]
 
    @property
    def bbox(self):
        return self.border.extent
 
    def save(self, *args, **kwargs):
        # New instance, or existing one whose border geometry changed?
        border_changed = True
        if self.pk:
            old_border = (
                InitialBorder.objects.filter(pk=self.pk)
                .values_list("border", flat=True)
                .first()
            )
            if old_border is not None:
                border_changed = old_border != self.border
 
        with transaction.atomic():
            super().save(*args, **kwargs)
 
            if border_changed:
                intersecting = Province.objects.filter(
                    border__intersects=self.border
                )
                # set() replaces existing relations, so no need for clear()
                self.province.set(intersecting)
 
    def __str__(self):
        return self.title
 
    class Meta:
        verbose_name = "لیست محدوده اولیه"
        verbose_name_plural = "لیست محدوده‌های اولیه"



#Attachment
from .attachment import *