from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from contracts.models.models import (
    ContractDomin,
    Contract,
    ContractElhaghye,
)
from contracts.models.SharhKhadamats import (
    ShrhBase,
    ShrhLayer,
)
from contracts.models.comments import (
    Comment,
)
from contracts.models.attachment import (

    ContractAttachment,
    ContractAttachmentDomain,

    SharhbaseAttachment,
    SharhbaseAttachmentDomain,
)
from initialborders.models.models import InitialBorder

class ContractDominAdmin(admin.ModelAdmin):
    list_display = ['title' , 'code']
class InitialBorderInline(admin.TabularInline):
    """Shows the initial borders that belong to a contract."""
    model = InitialBorder
    fk_name = "contract"
    fields = ['title', 'dtyp']
    autocomplete_fields = ['dtyp']
    extra = 0
    show_change_link = True
 
 
@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'dtyp', 'number', 'start_date', 'end_date',
        'progress', 'is_completed', 'initborders_count',
    ]
    search_fields = ['title', 'number']
    list_select_related = ['dtyp']
    autocomplete_fields = ['dtyp', 'company']
    inlines = [InitialBorderInline]
 
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('initborders')
 
    @admin.display(description="تعداد محدوده‌ها")
    def initborders_count(self, obj):
        # uses the prefetched data, so no extra query per row
        return len(obj.initborders.all())

class ContractElhaghyeAdmin(admin.ModelAdmin):
    list_display = ['title', 'contract__title', 'mablagh', 'tarikh']
    search_fields = ['title', 'contract__title']
    list_filter = ['tarikh']
    autocomplete_fields = ['contract']

class ShrhBaseAdmin(admin.ModelAdmin):
    list_display = ['contract' , 'title','faz','percentage','worked_percentage', ]
    search_fields = ['title']
    autocomplete_fields = ['contract']
class ShrhLayerAdmin(admin.ModelAdmin):
    list_display = ['shrh_base' , 'is_uploaded', 'last_uploaded_date', 'upload_count', 'is_verified', 'verified_by', 'verified_at']
    search_fields = ['shrh_base__title','layer_name__layername_en','layer_name__layername_fa']
    autocomplete_fields = ['shrh_base','layer_name',]
class CommentAdmin(admin.ModelAdmin):
    list_display = ['sharhlayer' , 'writer' , 'created_at']
    search_fields = []

class ContractAttachmentAdmin(admin.ModelAdmin):
    autocomplete_fields = ["contract"]

class ContractAttachmentDomainAdmin(admin.ModelAdmin):
    list_display = ['code' , 'name_en' , 'name_fa']
    search_fields = ['code' , 'name_en' , 'name_fa']

class SharhbaseAttachmentAdmin(admin.ModelAdmin):
    pass

class SharhbaseAttachmentDomainAdmin(admin.ModelAdmin):
    list_display = ['code' , 'name_en' , 'name_fa']
    search_fields = ['code' , 'name_en' , 'name_fa']

    
admin.site.register(ContractDomin,ContractDominAdmin)
admin.site.register(Contract,ContractAdmin)
admin.site.register(ContractElhaghye, ContractElhaghyeAdmin)

admin.site.register(ShrhBase , ShrhBaseAdmin)
admin.site.register(ShrhLayer , ShrhLayerAdmin)

admin.site.register(Comment , CommentAdmin)


admin.site.register(ContractAttachment , ContractAttachmentAdmin)
admin.site.register(ContractAttachmentDomain , ContractAttachmentDomainAdmin)

admin.site.register(SharhbaseAttachment , SharhbaseAttachmentAdmin)
admin.site.register(SharhbaseAttachmentDomain , SharhbaseAttachmentDomainAdmin)