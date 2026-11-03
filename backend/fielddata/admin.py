# from django.contrib import admin
# from django.utils.html import format_html

# from fielddata.models.models import (
#     ContractStep,
#     GeochemistaryFieldData,
# )


# # ==============================
# # ContractStep
# # ==============================
# @admin.register(ContractStep)
# class ContractStepAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "title",
#         "dtyp",
#         "created_at",
#     )
#     list_filter = ("dtyp",)
#     search_fields = ("title",)
#     ordering = ("id",)
#     readonly_fields = ("created_at", "updated_at")


# @admin.register(GeochemistaryFieldData)
# class GeochemistaryFieldDataAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "dstep__title",
#         "contract__title",
#         "created_at"
#     )
#     search_fields = ("contract__title",)
#     ordering = ("id",)
#     readonly_fields = ("created_at", "updated_at")
