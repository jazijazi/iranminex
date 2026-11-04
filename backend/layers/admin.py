from django.contrib import admin

from layers.models.models import (
    LayersNames,
    FeatureAttachment,
)

class LayerNameAdmin(admin.ModelAdmin):
    list_display = ['dtyp','lyrgroup_en','lyrgroup_fa','layername_en','layername_fa','geometrytype',]
    search_fields = ['lyrgroup_en' , 'lyrgroup_fa' , 'layername_en' , 'layername_fa']

class FeatureAttachmentAdmin(admin.ModelAdmin):
    list_display = ['pk' , 'upload_date' , 'file']

admin.site.register(LayersNames , LayerNameAdmin)
admin.site.register(FeatureAttachment , FeatureAttachmentAdmin)