from django.contrib import admin

from .models import Avatar


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ("get_user_name", "classe", "nivel", "xp_total", "moedas")
    list_filter = ("classe",)
    ordering = ("-xp_total",)

    def get_user_name(self, obj):
        """Return the avatar owner's full name or username."""
        return obj.user.get_full_name() or obj.user.username

    get_user_name.short_description = "Nome do usuário"
