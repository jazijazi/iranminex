from django.db import models
from django.contrib.gis.db import models as gis_models

from common.models import CustomModel , Province

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
        null=False
    )
    dtyp = models.ForeignKey(
        InitialBorderDomin,
        on_delete=models.SET_NULL,
        related_name="rinitialborderdomin",
        blank=True,
        null=True
    )
    oldid = models.IntegerField( # the is for migrate from old to new db
        primary_key=False,
        unique=False,
        blank=True,
        null=True
    )
    parentid = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name="rparentinitialborder",
        blank=True,
        null=True
    )
    border = gis_models.MultiPolygonField(
        srid=4326,
        blank=False,
        null=False
    )
    province = models.ManyToManyField(
        Province,
        verbose_name="استان",
        related_name="rprovinceinitialborder",
        blank=True
    )
    
    @property
    def center(self):
        return [self.border.centroid.x , self.border.centroid.y]
    
    @property
    def bbox(self):
        return self.border.extent
    
    def save(self, *args, **kwargs):
        # Check if this is a new instance or if border has changed
        border_changed = True
        if self.pk: #have pk menase its just update not create
            old_instance = InitialBorder.objects.get(pk=self.pk)
            border_changed = old_instance.border != self.border
        
        # Save the instance first
        super().save(*args, **kwargs)
        
        # Only recalculate provinces if border changed or new instance
        if border_changed:
            # Clear existing province relationships
            self.province.clear()
            
            # Find all provinces that intersect with this border
            intersecting_provinces = Province.objects.filter(
                border__intersects=self.border
            )
            
            # Add the intersecting provinces to the M2M relationship
            self.province.set(intersecting_provinces)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "لیست محدوده اولیه"
        verbose_name_plural = "لیست  محدوده های اولیه"



#Metadata
from .metadata import *

#Attachment
from .attachment import *