from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from initialborders.models.models import (
    InitialBorder,
    InitialBorderDomin,
    #Attachment
    InitialBorderAttachment,
    InitialBorderAttachmentDomain,
    #Metadata
    InitialBorderMetadataPahneh,
    InitialBorderMetadataDarkhastekteshaf,
    InitialBorderMetadataParvaneekteshaf,
    InitialBorderMetadataGovahikashf,
    InitialBorderMetadataParvanebahrebardai,
    InitialBorderMetadataPotansielyabi,
    InitialBorderMetadataCoal
)
from initialborders.models.amar import (
    AmarKarKhaneh,
    AmarEstekhraj,
    HSEPASMAND,
    HSEHADESE,
    AmarEkteshaf,
    AmarAmalkardBahrebardariCoal,
    AmarAmalkardTajhizCoal,
)
from initialborders.models.ipcamar import (
    IpcAmarEkteshaf,
    IpcBarnamehEkteshaf,
)

admin.site.site_header = 'مدیریت سامانه'
admin.site.index_title = 'صفحه مدیریت'

class InitialBorderAdmin(LeafletGeoAdmin):
    search_fields = ['title', 'dtyp__title']
    list_filter = ['dtyp']
    list_display = ['id','title','dtyp','parentid']

class InitialBorderDominModalAdmin(admin.ModelAdmin):
    list_display = ['id','title','code']

class InitialBorderAttachmentModalAdmin(admin.ModelAdmin):
    autocomplete_fields = ['rinitialborder']

class InitialBorderAttachmentDomainModalAdmin(admin.ModelAdmin):
    list_display = ['id','code' , 'name' , 'category' , 'dinitialborder']

class AmarKarKhanehAdmin(admin.ModelAdmin):
    list_display = ("initialborder","sal","doure","name_mahsoul",)
    search_fields = ("name_mahsoul", "initialborder__title")
    autocomplete_fields = ("initialborder",)
    list_select_related = ("initialborder",)
    ordering = ("-sal", "-doure")

    fieldsets = (
        ("اطلاعات پایه", {
            "fields": ("initialborder", "sal", "doure", "name_mahsoul")
        }),
        ("تولید و ظرفیت", {
            "fields": (
                "zarfiyat_amaliyati",
                "mahsoul_kham_daryafti",
                "mizain_toulid",
                "hazine_toulid",
            )
        }),
        ("مصرف انرژی و مواد", {
            "fields": (
                "masraf_ab",
                "masraf_bargh",
                "masraf_soukht",
                "masraf_gaz",
                "masraf_mavad",
            )
        }),
    )

class AmarEstekhrajAdmin(admin.ModelAdmin):
    list_display = ("initialborder","sal","doure",)
    search_fields = ("initialborder__title",)
    autocomplete_fields = ("initialborder",)
    list_select_related = ("initialborder",)
    ordering = ("-sal", "-doure")

    fieldsets = (
        ("اطلاعات پایه", {
            "fields": ("initialborder", "sal", "doure")
        }),
        ("استخراج و عیار", {
            "fields": (
                "made_madani_estekhraji",
                "ayar_made_madani",
                "estekhraj_vaghei",
                "motavaset_ayar_estekhraji",
                "mizan_batele_bardari",
            )
        }),
        ("هزینه و عملکرد", {
            "fields": ("hazine_estekhraj", "darsad_amalkard")
        }),
    )

class HSEPASMANDAdmin(admin.ModelAdmin):
    list_display = ("initialborder","sal","doure",)
    search_fields = ("onvan_pasmand", "initialborder__title")
    autocomplete_fields = ("initialborder",)
    list_select_related = ("initialborder",)
    ordering = ("-sal", "-doure")

class HSEHADESEAdmin(admin.ModelAdmin):
    list_display = ("initialborder","sal",)
    search_fields = ("initialborder__title",)
    autocomplete_fields = ("initialborder",)
    list_select_related = ("initialborder",)
    ordering = ("-sal",)

class AmarEkteshafAdmin(admin.ModelAdmin):
    list_display = ("initialborder","sal","doure",)
    search_fields = ("initialborder__title",)
    autocomplete_fields = ("initialborder",)
    list_select_related = ("initialborder",)
    ordering = ("-sal", "-doure")

class AmarAmalkardBahrebardariCoalAdmin(admin.ModelAdmin):
    list_display = ("initialborder","sal","doure",)
    search_fields = ("initialborder__title",)
    autocomplete_fields = ("initialborder",)
    list_select_related = ("initialborder",)
    ordering = ("-sal", "-doure")

class AmarAmalkardTajhizCoalAdmin(admin.ModelAdmin):
    list_display = ("initialborder","sal","doure",)
    search_fields = ("initialborder__title",)
    autocomplete_fields = ("initialborder",)
    list_select_related = ("initialborder",)
    ordering = ("-sal", "-doure")

class IpcAmarEkteshafAdmin(admin.ModelAdmin):
    list_display = ("initialborder","sal","doure",'faz','shakhes')
    search_fields = ("initialborder__title",)
    autocomplete_fields = ("initialborder",)
    list_select_related = ("initialborder",)
    ordering = ("-sal", "-doure")


class IpcBarnamehEkteshafAdmin(admin.ModelAdmin):
    list_display = ("sal","faz","shakhes","vahed")
    ordering = ("-sal",)

admin.site.register(InitialBorder , InitialBorderAdmin)
admin.site.register(InitialBorderDomin , InitialBorderDominModalAdmin)
#Attachment
admin.site.register(InitialBorderAttachment , InitialBorderAttachmentModalAdmin)
admin.site.register(InitialBorderAttachmentDomain , InitialBorderAttachmentDomainModalAdmin)
#Metadata
admin.site.register(InitialBorderMetadataPahneh)
admin.site.register(InitialBorderMetadataDarkhastekteshaf)
admin.site.register(InitialBorderMetadataParvaneekteshaf)
admin.site.register(InitialBorderMetadataGovahikashf)
admin.site.register(InitialBorderMetadataParvanebahrebardai)
admin.site.register(InitialBorderMetadataPotansielyabi)
admin.site.register(InitialBorderMetadataCoal)
# AMAR
admin.site.register(AmarKarKhaneh , AmarKarKhanehAdmin)
admin.site.register(AmarEstekhraj , AmarEstekhrajAdmin)
admin.site.register(HSEPASMAND , HSEPASMANDAdmin)
admin.site.register(HSEHADESE , HSEHADESEAdmin)
admin.site.register(AmarEkteshaf , AmarEkteshafAdmin)
admin.site.register(AmarAmalkardBahrebardariCoal , AmarAmalkardBahrebardariCoalAdmin)
admin.site.register(AmarAmalkardTajhizCoal , AmarAmalkardTajhizCoalAdmin)

admin.site.register(IpcAmarEkteshaf,IpcAmarEkteshafAdmin)
admin.site.register(IpcBarnamehEkteshaf,IpcBarnamehEkteshafAdmin)
