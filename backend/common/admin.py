import json
from django.contrib import admin 
from django.utils.html import format_html
from leaflet.admin import LeafletGeoAdmin
from common.models.other import NoeKhadamat, Sherkat
from common.models.districts import (
    Ostan,
    Shahrestan,
)
from common.models.models import (
    DeletionLog
)


class OstanAdmin(LeafletGeoAdmin):
    list_display = ('title' , 'code')
    search_fields = ['title','code']
class ShahrestanAdmin(LeafletGeoAdmin):
    list_display = ('title' , 'code' , 'ostan__title')
    search_fields = ['title','code']
class NoeKhadamatAdmin(admin.ModelAdmin):
    """نوع خدمات (اکتشاف، حفاری، ...). search_fields برای autocomplete شرکت‌ها لازم است."""
    list_display = ("title", "tedad_sherkat")
    search_fields = ("title",)
    ordering = ("title",)

    @admin.display(description="تعداد شرکت‌ها")
    def tedad_sherkat(self, obj):
        return obj.rSherkatha.count()

class SherkatAdmin(admin.ModelAdmin):
    """لیست شرکت‌ها؛ فیلتر روی «مجاز به مشاور ارشد» و نوع خدمات."""
    list_display = ("name", "code", "typ", "khadamat", "mojaz_moshaver_arshad", "callnumber")
    list_filter = ("mojaz_moshaver_arshad", "noe_khadamat", "typ")
    list_editable = ("mojaz_moshaver_arshad",)
    search_fields = ("name", "code", "callnumber")
    filter_horizontal = ("noe_khadamat",)
    list_per_page = 30
    fieldsets = (
        ("مشخصات شرکت", {"fields": ("name", "code", "typ")}),
        ("خدمات و دسترسی", {"fields": ("noe_khadamat", "mojaz_moshaver_arshad")}),
        ("اطلاعات تماس", {"fields": ("callnumber", "address", "comment")}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("noe_khadamat")

    @admin.display(description="نوع خدمات")
    def khadamat(self, obj):
        return "، ".join(k.title for k in obj.noe_khadamat.all()) or "—"
class DeletionLogAdmin(admin.ModelAdmin):
    """
    Browsable but tamper-proof: nobody can create or edit entries here, and
    only superusers can delete them. Editing a deletion record would defeat
    the point of an audit trail, so this intentionally isn't a normal
    CRUD admin.
    """
 
    list_display = ("deleted_at", "object_label", "deleted_by", "ip_address", "data_preview")
    date_hierarchy = "deleted_at"
    search_fields = ("=object_id", "deleted_by__username", "ip_address")
    list_select_related = ("content_type", "deleted_by")
    ordering = ("-deleted_at",)
 
    # Field order for the detail page. Listed explicitly (not "__all__")
    # so pretty_data - a display-only method, not a real model field -
    # renders where the raw `data` column would otherwise sit.
    fields = ("content_type", "object_id", "deleted_at", "deleted_by", "ip_address", "pretty_data")
    readonly_fields = fields
  
    @admin.display(description="شیء حذف‌شده", ordering="object_id")
    def object_label(self, obj):
        return f"{obj.content_type.model} #{obj.object_id}"
 
    @admin.display(description="داده (خلاصه)")
    def data_preview(self, obj):
        raw = json.dumps(obj.data, ensure_ascii=False)
        return (raw[:80] + "…") if len(raw) > 80 else raw
 
    @admin.display(description="داده کامل")
    def pretty_data(self, obj):
        pretty = json.dumps(obj.data, indent=2, ensure_ascii=False)
        return format_html("<pre style='white-space: pre-wrap; margin: 0'>{}</pre>", pretty)
 

admin.site.register(Ostan, OstanAdmin)
admin.site.register(Shahrestan, ShahrestanAdmin)
admin.site.register(Sherkat, SherkatAdmin)
admin.site.register(NoeKhadamat, NoeKhadamatAdmin)
admin.site.register(DeletionLog, DeletionLogAdmin)