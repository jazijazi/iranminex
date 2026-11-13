from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from initialborders.models.models import (
    InitialBorder,
    InitialBorderMadeDomin,
    InitialBorderDomin,
    ContractInitialBorder,
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

class InitialBorderMadeDominInline(admin.TabularInline):
    model = InitialBorderMadeDomin
    extra = 1

class InitialBorderAttachmentDomainInline(admin.TabularInline):
    model = InitialBorderAttachmentDomain
    extra = 1

class ContractInitialBorderInline(admin.TabularInline):
    model = ContractInitialBorder
    fk_name = "initial_border"
    extra = 1
    autocomplete_fields = ["contract"]

class InitialBorderAdmin(LeafletGeoAdmin):
    search_fields = ["title", "dtyp__title", "contracts__title"]
    list_filter = ["dtyp", "ostan"]
    list_display = ["id", "title", "display_contracts", "dtyp", "display_ostans"]
    list_select_related = ["dtyp", "made"]
    autocomplete_fields = ["dtyp","made"]
    inlines = [ContractInitialBorderInline, InitialBorderAttachmentInline]
    readonly_fields = ["ostan"]

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .select_related("dtyp",)
            .prefetch_related("ostan", "contracts")
        )

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term
        )
        # searching through contracts__title can return the same row twice
        return queryset, True

    @admin.display(description="استان‌ها")
    def display_ostans(self, obj):
        return ", ".join(p.name_fa for p in obj.ostan.all())

    @admin.display(description="قراردادها")
    def display_contracts(self, obj):
        return ", ".join(c.title for c in obj.contracts.all())
class InitialBorderDominModalAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'code']
    search_fields = ['title', 'code']
    inlines = [InitialBorderAttachmentDomainInline]

class InitialBorderMadeDominAdmin(admin.ModelAdmin):
    list_display = ['id', 'title',]
    search_fields = ['title',]

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
admin.site.register(InitialBorderMadeDomin , InitialBorderMadeDominAdmin)
#Attachment
admin.site.register(InitialBorderAttachment , InitialBorderAttachmentModalAdmin)
admin.site.register(InitialBorderAttachmentDomain , InitialBorderAttachmentDomainModalAdmin)
