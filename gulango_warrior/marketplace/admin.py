from django.contrib import admin

from .models import Item, CompraItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco", "classe_restrita")


@admin.register(CompraItem)
class CompraItemAdmin(admin.ModelAdmin):
    list_display = ("avatar", "item", "data_compra")
