from django.contrib import admin
from .models import Ware, Factor


class WareAdmin(admin.ModelAdmin):
    list_display = ("name", "cost_method")
    list_filter = ("cost_method",)
    search_fields = ("name",)
    ordering = ("name",)


class FactorAdmin(admin.ModelAdmin):
    list_display = (
        "ware",
        "type",
        "quantity",
        "purchase_price",
        "total_cost",
        "created_at",
    )
    list_filter = ("type", "ware__name", "created_at")
    search_fields = ("ware__name",)
    ordering = ("-created_at",)


admin.site.register(Ware, WareAdmin)
admin.site.register(Factor, FactorAdmin)
