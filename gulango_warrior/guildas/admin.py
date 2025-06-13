from django.contrib import admin

from .models import Guilda


@admin.register(Guilda)
class GuildaAdmin(admin.ModelAdmin):
    list_display = ("nome", "lider", "data_criacao")
    search_fields = ("nome", "lider__username")
    ordering = ("-data_criacao",)
