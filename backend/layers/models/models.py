import os
import uuid
from pathlib import Path
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from django.db import models

from contracts.models.models import (
    ContractDomin,
)
# from contracts.models.SharhKhadamats import ShrhLayer

class LayersNames(models.Model):
    dtyp = models.ForeignKey(
        ContractDomin,
        on_delete=models.SET_NULL,
        related_name="rlyrnamedtyp",
        blank=True,
        null=True,
    )
    lyrgroup_en = models.CharField(
        max_length=40,
        unique=False,
        blank=True,
        null=True,
    )
    lyrgroup_fa = models.CharField(
        max_length=40,
        unique=False,
        blank=True,
        null=True,
    )
    layername_en = models.CharField(
        max_length=40,
        unique=False,
        blank=True,
        null=True,
    )
    layername_fa = models.CharField(
        max_length=40,
        unique=False,
        blank=True,
        null=True,
    )
    geometrytype = models.CharField(
        max_length=20,
        unique=False,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.lyrgroup_en} --- {self.layername_en} --- ({self.geometrytype})"
    
    class Meta:
        verbose_name = "لیست نام لایه ها"
        verbose_name_plural = "لیست نام لایه ها"

class CommonFields(models.Model):
    id_code = models.CharField(max_length=50 , unique=False,blank=True,null=True)
    id_area = models.CharField(max_length=50 , unique=False,blank=True,null=True)
    information = models.CharField(max_length=100 , unique=False,blank=True,null=True)

    class Meta:
        abstract = True
class LinkedToLayerTable(CommonFields):
    """
        This little guy holds all the layer tables together. Treat it like a sleeping dragon!
    """
    shr_layer = models.ForeignKey(
        "contracts.ShrhLayer",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='%(class)s_rshrlayer',
        db_index=True
    )

    class Meta:
        abstract = True

def dynamic_upload_path(instance, filename):
    name, ext = os.path.splitext(filename)
    safe_filename = f"{uuid.uuid4().hex[:8]}_{name[:50]}{ext}"
    
    return f'prjapi/featureattachment/{instance.content_type.model}/{instance.object_id}/{safe_filename}'

def validate_file_size(file):
    """Validate file size (max 300MB)"""
    max_size = 300 * 1024 * 1024  # 300MB
    if file.size > max_size:
        raise ValidationError('File size cannot exceed 300MB.')
class FeatureAttachmentManager(models.Manager):
    """Custom manager for FeatureAttachment"""
    
    def for_object(self, obj):
        """Get all attachments for a specific object"""
        content_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type=content_type, object_id=obj.pk)
    
class FeatureAttachment(models.Model):
    """
    Generic attachment model that can be linked to any model instance.
    Supports file upload with validation and automatic cleanup.
    """
    
    upload_date = models.DateTimeField(
        verbose_name="تاریخ ساخت",
        auto_now_add=True,
        db_index=True  # Add index for better query performance
    )
    
    writer = models.ForeignKey(
        'accounts.User', 
        on_delete=models.SET_NULL, 
        related_name="user_featureattachment", 
        blank=True, 
        null=True,
        verbose_name="نویسنده",
        db_index=True  # Add index for better query performance
    )
    
    # Generic foreign key fields
    # These three fields work together to create the Generic Foreign Key
    # fields: (content_type,object_id,linked_to_project)
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        db_index=True
    )
    object_id = models.PositiveIntegerField(
        db_index=True
    )
    linked_to_project = GenericForeignKey('content_type', 'object_id')

    # File field with validation
    file = models.FileField(
        verbose_name="فایل",
        blank=False,
        upload_to=dynamic_upload_path,
        validators=[validate_file_size],
    )
    
    # Optional: Add file description
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="توضیحات",
    )
        
    # Add custom manager
    objects = FeatureAttachmentManager()
    
    class Meta:
        verbose_name = "اتچمنت عارضه"
        verbose_name_plural = "اتچمنت های عارضه"
        
        indexes = [
            models.Index(fields=['content_type', 'object_id']),  # Composite index for generic FK
            models.Index(fields=['-upload_date']),  # Index for date ordering
        ]
        
        # Add ordering
        ordering = ['-upload_date']
    
    def clean(self):
        """Additional validation"""
        super().clean()
        
        # Validate that the linked object exists
        if self.content_type and self.object_id:
            try:
                model_class = self.content_type.model_class()
                model_class.objects.get(pk=self.object_id)
            except model_class.DoesNotExist:
                raise ValidationError('The linked object does not exist.')
    
    def save(self, *args, **kwargs):
        """Override save to store file size"""
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """Delete file from filesystem when model instance is deleted"""
        self.delete_file()
        super().delete(*args, **kwargs)
    
    def delete_file(self):
        """Helper method to delete the physical file"""
        if self.file:
            file_path = Path(self.file.path)
            if file_path.exists() and file_path.is_file():
                try:
                    file_path.unlink()  # More modern than os.remove
                except (OSError, PermissionError) as e:
                    # Log the error instead of failing silently
                    # import logging
                    # logger = logging.getLogger(__name__)
                    # logger.error(f"Failed to delete file {file_path}: {e}")
                    print("Error Delete the File From Feature Attachment Database Table")
    
    def __str__(self):
        """String representation"""
        if self.file:
            filename = os.path.basename(self.file.name)
            return f"{self.upload_date.strftime('%Y-%m-%d')} - {filename}"
        return f"Attachment {self.pk} - {self.upload_date}"


# IMPORT LAYERS
# from .layermodels.coal_layers import *
# from .layermodels.excavation_layer import *
# from .layermodels.general_layer import *
# from .layermodels.geochemistry_layer import *
# from .layermodels.geology import *
# from .layermodels.geology_section_layer import *
# from .layermodels.geophysic_layer import *
# from .layermodels.geophysic_section_layer import *
# from .layermodels.remotesensing_layer import *
# from .layermodels.topography_layer import *
# from .layermodels.mining_equipment_layer import *

# from .layermodels.extraction import *
# from .layermodels.factory import *