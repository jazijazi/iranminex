from django.contrib import admin, messages
from django.contrib.gis import admin as gis_admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from common.models.other import Sherkat
from initialborders.models.models import InitialBorder

from contracts.models.comments import (
    Comment,
)
from contracts.models.attachment import (

    ContractAttachment,
    ContractAttachmentDomain,

    SharhbaseAttachment,
    SharhbaseAttachmentDomain,
)
from contracts.models.models import (
    Contract, ContractDomin, ContractElhaghye,
    Faz, Vahed, ShrhCatalog,
    NaghshSherkat, SherkatContract,
    EkhtesasShrh, ShrhContract, ShrhLayer,
)


    
class InitialBorderInline(admin.TabularInline):
    """Shows the initial borders that belong to a contract."""
    model = InitialBorder
    fk_name = "contract"
    fields = ['title', 'dtyp']
    autocomplete_fields = ['dtyp']
    extra = 0
    show_change_link = True

@admin.register(ContractElhaghye)
class ContractElhaghyeAdmin(admin.ModelAdmin):
    list_display = ['title', 'contract__title', 'mablagh', 'tarikh']
    search_fields = ['title', 'contract__title']
    list_filter = ['tarikh']
    autocomplete_fields = ['contract']

@admin.register(ContractAttachment)

class ContractAttachmentAdmin(admin.ModelAdmin):
    autocomplete_fields = ["contract"]

@admin.register(ContractAttachmentDomain)

class ContractAttachmentDomainAdmin(admin.ModelAdmin):
    list_display = ['code' , 'name_en' , 'name_fa']
    search_fields = ['code' , 'name_en' , 'name_fa']

# ───────────────────────── ابزار نمایش ─────────────────────────

def progress_bar(value):
    """نوار پیشرفت کوچک (۰ تا ۱۰۰) برای ستون‌های لیست."""
    value = max(0, min(float(value or 0), 100))
    color = "#16a34a" if value >= 100 else "#2563eb" if value >= 40 else "#d97706"
    return format_html(
        '<div style="min-width:110px;background:#e5e7eb;border-radius:6px;overflow:hidden;">'
        '<div style="width:{w}%;background:{c};color:#fff;font-size:11px;'
        'padding:1px 6px;white-space:nowrap;">{t}%</div></div>',
        w=f"{value:.0f}", c=color, t=f"{value:.0f}",
    )


def badge(text, color):
    return format_html(
        '<span style="background:{c};color:#fff;padding:2px 8px;border-radius:10px;'
        'font-size:11px;">{t}</span>', c=color, t=text,
    )


# ───────────────────────── جداول پایه ─────────────────────────

@admin.register(ContractDomin)
class ContractDominAdmin(admin.ModelAdmin):
    list_display = ("code", "title")
    search_fields = ("title",)
    ordering = ("code",)


@admin.register(Faz)
class FazAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "tedad_band")
    list_editable = ("order",)
    search_fields = ("title",)

    @admin.display(description="تعداد بندها")
    def tedad_band(self, obj):
        return obj.rbandha.count()


@admin.register(Vahed)
class VahedAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(NaghshSherkat)
class NaghshSherkatAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


# ───────────────────────── کاتالوگ شرح خدمات ─────────────────────────

@admin.register(ShrhCatalog)
class ShrhCatalogAdmin(admin.ModelAdmin):
    """درخت کاتالوگ اکسل: گروه‌ها پررنگ و بندها با تورفتگی نمایش داده می‌شوند."""
    list_display = ("code", "onvan", "faz", "vahed", "noe", "order")
    list_display_links = ("code", "onvan")
    list_filter = ("faz", "is_group", "vahed")
    search_fields = ("title", "code", "description")
    autocomplete_fields = ("parent", "vahed")
    list_select_related = ("faz", "vahed", "parent")
    ordering = ("faz__order", "order")
    list_per_page = 60
    fieldsets = (
        ("جایگاه در درخت", {"fields": ("faz", "parent", "is_group", "code", "order")}),
        ("مشخصات بند", {"fields": ("title", "vahed", "description")}),
    )

    @admin.display(description="عنوان", ordering="title")
    def onvan(self, obj):
        if obj.is_group:
            return format_html("<strong>{}</strong>", obj.title)
        pad = 18 if obj.parent_id else 0
        return format_html('<span style="padding-right:{}px">↳ {}</span>', pad, obj.title)

    @admin.display(description="نوع")
    def noe(self, obj):
        return badge("گروه", "#7c3aed") if obj.is_group else badge("بند", "#0891b2")


# ───────────────────────── شرکت‌های قرارداد ─────────────────────────

@admin.register(SherkatContract)
class SherkatContractAdmin(admin.ModelAdmin):
    list_display = ("sherkat", "naghsh", "contract", "tedad_ekhtesas")
    list_filter = ("naghsh",)
    search_fields = ("sherkat__name", "contract__title", "contract__number")
    autocomplete_fields = ("contract", "sherkat")
    list_select_related = ("sherkat", "naghsh", "contract")

    @admin.display(description="تعداد بسته‌ها")
    def tedad_ekhtesas(self, obj):
        return obj.rekhtesasha.count()


# ───────────────────────── اختصاص (بستهٔ کار + کادر) ─────────────────────────

class BandBasteInline(admin.TabularInline):
    """بندهای یک بسته (فقط‌خواندنی؛ اختصاص از صفحهٔ «بندهای قرارداد» انجام می‌شود)."""
    model = ShrhContract
    fk_name = "ekhtesas"
    extra = 0
    can_delete = False
    fields = ("shrh_catalog", "scale", "percentage", "worked_percentage")
    readonly_fields = fields
    verbose_name = "بند"
    verbose_name_plural = "بندهای این بسته"

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(EkhtesasShrh)
class EkhtesasShrhAdmin(gis_admin.GISModelAdmin):
    list_display = ("__str__", "contract_title", "scale", "tedad_band", "vazn", "pishraft_bar", "assigned_by")
    list_filter = ("scale", "sherkat_contract__naghsh")
    search_fields = ("kader_name", "sherkat_contract__sherkat__name", "sherkat_contract__contract__title")
    autocomplete_fields = ("sherkat_contract",)
    list_select_related = ("sherkat_contract__sherkat", "sherkat_contract__contract", "assigned_by")
    readonly_fields = ("assigned_by",)
    inlines = [BandBasteInline]
    fieldsets = (
        ("شرکت و کادر", {"fields": ("sherkat_contract", "kader_name", "scale", "kader")}),
        ("ثبت", {"fields": ("assigned_by",)}),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.assigned_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description="قرارداد")
    def contract_title(self, obj):
        return obj.contract.title

    @admin.display(description="تعداد بندها")
    def tedad_band(self, obj):
        return obj.rbandha.count()

    @admin.display(description="مجموع وزن")
    def vazn(self, obj):
        return f"{obj.vazn_kol:g}٪"

    @admin.display(description="پیشرفت")
    def pishraft_bar(self, obj):
        return progress_bar(obj.pishraft)


# ───────────────────────── بندهای شرح خدمات قرارداد ─────────────────────────

@admin.register(ShrhContract)
class ShrhContractAdmin(admin.ModelAdmin):
    list_display = ("contract", "band", "scale", "percentage", "completion_bar", "sherkat", "ekhtesas_vaziat")
    list_filter = ("scale", "shrh_catalog__faz", "contract")
    search_fields = ("contract__title", "shrh_catalog__title", "shrh_catalog__code")
    autocomplete_fields = ("contract", "shrh_catalog", "ekhtesas")
    list_select_related = ("contract", "shrh_catalog", "ekhtesas__sherkat_contract__sherkat")
    list_per_page = 40
    actions = ["khali_kardan_ekhtesas"]
    fieldsets = (
        ("قرارداد و بند", {"fields": ("contract", "shrh_catalog", "scale")}),
        ("وزن و پیشرفت", {"fields": ("percentage", "worked_percentage")}),
        ("اختصاص", {"fields": ("ekhtesas",)}),
    )

    @admin.display(description="بند", ordering="shrh_catalog__title")
    def band(self, obj):
        return obj.shrh_catalog.title

    @admin.display(description="پیشرفت")
    def completion_bar(self, obj):
        return progress_bar(obj.completion_percentage)

    @admin.display(description="شرکت")
    def sherkat(self, obj):
        return obj.ekhtesas.sherkat_contract.sherkat if obj.ekhtesas_id else "—"

    @admin.display(description="وضعیت اختصاص")
    def ekhtesas_vaziat(self, obj):
        return badge("اختصاص‌یافته", "#16a34a") if obj.ekhtesas_id else badge("بدون اختصاص", "#6b7280")

    @admin.action(description="خالی کردن اختصاص بندهای انتخاب‌شده")
    def khali_kardan_ekhtesas(self, request, queryset):
        n = queryset.update(ekhtesas=None)
        self.message_user(request, f"اختصاص {n} بند برداشته شد.", messages.SUCCESS)


# ───────────────────────── لایه‌ها ─────────────────────────

@admin.register(ShrhLayer)
class ShrhLayerAdmin(admin.ModelAdmin):
    """بارگذاری/تایید فقط با action تا کاربر و زمان همیشه درست ثبت شود."""
    list_display = ("__str__", "contract", "vaziat", "upload_count", "last_uploaded_by", "verified_by")
    list_filter = ("is_uploaded", "is_verified", "layer_name")
    search_fields = ("shrh_contract__shrh_catalog__title", "shrh_contract__contract__title", "raster_uuid")
    autocomplete_fields = ("shrh_contract", "layer_name")
    list_select_related = ("shrh_contract__contract", "shrh_contract__shrh_catalog", "layer_name",
                           "last_uploaded_by", "verified_by")
    readonly_fields = ("is_uploaded", "last_uploaded_date", "last_uploaded_by", "upload_count",
                       "is_verified", "verified_by", "verified_at")
    actions = ["action_uploaded", "action_verify"]
    fieldsets = (
        ("لایه", {"fields": ("shrh_contract", "layer_name", "raster_uuid")}),
        ("اندازه و قیمت", {"fields": ("layer_weight", "layer_volume", "unit_price")}),
        ("بارگذاری", {"fields": ("is_uploaded", "last_uploaded_date", "last_uploaded_by", "upload_count")}),
        ("تایید نهایی", {"fields": ("is_verified", "verified_by", "verified_at")}),
    )

    @admin.display(description="قرارداد")
    def contract(self, obj):
        return obj.shrh_contract.contract.title

    @admin.display(description="وضعیت")
    def vaziat(self, obj):
        colors = {"تایید شده": "#16a34a", "بارگذاری شده": "#2563eb"}
        return badge(obj.status, colors.get(obj.status, "#6b7280"))

    @admin.action(description="ثبت به‌عنوان بارگذاری‌شده")
    def action_uploaded(self, request, queryset):
        for layer in queryset:
            layer.mark_as_uploaded(request.user)
        self.message_user(request, f"{queryset.count()} لایه بارگذاری‌شده ثبت شد.", messages.SUCCESS)

    @admin.action(description="تایید نهایی لایه‌ها")
    def action_verify(self, request, queryset):
        ok = 0
        for layer in queryset:
            try:
                layer.verify(request.user)
                ok += 1
            except ValidationError as e:
                self.message_user(request, f"{layer}: {'، '.join(e.messages)}", messages.WARNING)
        if ok:
            self.message_user(request, f"{ok} لایه تایید شد.", messages.SUCCESS)


# ───────────────────────── قرارداد ─────────────────────────

class SherkatContractInline(admin.TabularInline):
    model = SherkatContract
    extra = 0
    autocomplete_fields = ("sherkat",)
    verbose_name = "شرکت"
    verbose_name_plural = "شرکت‌های قرارداد (ناظر، پیمانکار، ...)"


class ShrhContractInline(admin.TabularInline):
    model = ShrhContract
    extra = 0
    autocomplete_fields = ("shrh_catalog",)
    fields = ("shrh_catalog", "scale", "percentage", "worked_percentage")
    verbose_name = "بند"
    verbose_name_plural = "شرح خدمات و وزن‌ها (توسط سازمان)"


class ElhaghyeInline(admin.TabularInline):
    model = ContractElhaghye
    extra = 0
    fields = ("title", "mablagh", "tarikh", "description")
    verbose_name_plural = "الحاقیه‌ها"


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("title", "number", "dtyp", "moshaver_arshad", "department",
                    "start_date", "end_date", "progress_bar", "is_completed")
    list_filter = ("is_completed", "dtyp", "department", "elhaghye")
    search_fields = ("title", "number", "moshaver_arshad__name")
    list_select_related = ("dtyp", "moshaver_arshad")
    date_hierarchy = "start_date"
    inlines = [SherkatContractInline, ShrhContractInline, ElhaghyeInline]
    fieldsets = (
        ("مشخصات قرارداد", {"fields": ("title", "number", "dtyp", "department", "moshaver_arshad")}),
        ("زمان‌بندی", {"fields": (("start_date", "end_date"), "progress", "is_completed")}),
        ("مالی", {"fields": ("mablagh", "elhaghye", "mablaghe_elhaghye", "tarikh_elhaghye")}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # فقط شرکت‌های مجاز برای مشاور ارشد در لیست انتخاب بیایند
        if db_field.name == "moshaver_arshad":
            kwargs["queryset"] = Sherkat.objects.filter(mojaz_moshaver_arshad=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.display(description="پیشرفت", ordering="progress")
    def progress_bar(self, obj):
        return progress_bar(obj.progress)