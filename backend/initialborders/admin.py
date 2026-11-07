from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from initialborders.models.models import (
    InitialBorder,
    InitialBorderDomin,
    #Attachment
    InitialBorderAttachment,
    InitialBorderAttachmentDomain
)

admin.site.site_header = 'مدیریت سامانه'
admin.site.index_title = 'صفحه مدیریت'

class InitialBorderAttachmentInline(admin.TabularInline):
    model = InitialBorderAttachment
    extra = 1
    autocomplete_fields = ['dtyp_attach']

class InitialBorderAttachmentDomainInline(admin.TabularInline):
    model = InitialBorderAttachmentDomain
    extra = 1

class InitialBorderAdmin(LeafletGeoAdmin):
    search_fields = ['title', 'dtyp__title', 'contract__title']
    list_filter = ['dtyp', 'ostan']
    list_display = ['id', 'title', 'contract', 'dtyp', 'parentid', 'display_ostans']
    list_select_related = ['contract', 'dtyp', 'parentid']
    autocomplete_fields = ['contract', 'parentid', 'dtyp']
    inlines = [InitialBorderAttachmentInline]
    readonly_fields = ['ostan']
 
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('ostan')
 
    @admin.display(description="استان‌ها")
    def display_ostans(self, obj):
        return ", ".join(p.name_fa for p in obj.ostan.all())


class InitialBorderDominModalAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'code']
    search_fields = ['title', 'code']
    inlines = [InitialBorderAttachmentDomainInline]

class InitialBorderAttachmentModalAdmin(admin.ModelAdmin):
    list_display = ['id', 'rinitialborder', 'dtyp_attach', 'upload_date', 'writer']
    list_filter = ['dtyp_attach', 'upload_date', 'writer']
    search_fields = ['rinitialborder__title', 'file']
    autocomplete_fields = ['rinitialborder', 'dtyp_attach']

class InitialBorderAttachmentDomainModalAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'category', 'dinitialborder']
    search_fields = ['name', 'code', 'category']
    list_filter = ['category', 'dinitialborder']
    autocomplete_fields = ['dinitialborder']

admin.site.register(InitialBorder , InitialBorderAdmin)
admin.site.register(InitialBorderDomin , InitialBorderDominModalAdmin)
#Attachment
admin.site.register(InitialBorderAttachment , InitialBorderAttachmentModalAdmin)
admin.site.register(InitialBorderAttachmentDomain , InitialBorderAttachmentDomainModalAdmin)
