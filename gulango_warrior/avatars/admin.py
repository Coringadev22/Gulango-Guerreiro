from django.contrib import admin

from .models import Avatar


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ("user", "classe", "nivel", "xp_total", "moedas")
