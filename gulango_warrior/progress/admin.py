from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import redirect
from django.utils.html import format_html

from .models import (
    LessonProgress,
    Conquista,
    AvatarConquista,
    MissaoDiaria,
    UsuarioMissao,
    ProgressoPorLinguagem,
)

admin.site.register(LessonProgress)
@admin.register(Conquista)
class ConquistaAdmin(admin.ModelAdmin):
    list_display = ("nome", "condicao", "avatarconquista_count")
admin.site.register(AvatarConquista)


@admin.register(MissaoDiaria)
class MissaoDiariaAdmin(admin.ModelAdmin):
    """Admin customization for :class:`MissaoDiaria`."""

    list_display = (
        "descricao",
        "xp_recompensa",
        "moedas_recompensa",
        "duplicate_button",
    )
    actions = ["duplicate_selected"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:missao_id>/duplicate/",
                self.admin_site.admin_view(self.duplicate_missao),
                name="progress_missaodiaria_duplicate",
            )
        ]
        return custom_urls + urls

    def duplicate_button(self, obj):
        url = reverse("admin:progress_missaodiaria_duplicate", args=[obj.pk])
        return format_html('<a class="button" href="{}">Duplicar missão</a>', url)

    duplicate_button.short_description = "Duplicar missão"
    duplicate_button.allow_tags = True

    def duplicate_missao(self, request, missao_id):
        missao = MissaoDiaria.objects.get(pk=missao_id)
        missao.pk = None
        missao.save()
        self.message_user(request, "Missão duplicada com sucesso.")
        return redirect("..")

    def duplicate_selected(self, request, queryset):
        for missao in queryset:
            missao.pk = None
            missao.save()
        self.message_user(request, "Missões duplicadas com sucesso.")

    duplicate_selected.short_description = "Duplicar missões selecionadas"

admin.site.register(UsuarioMissao)
admin.site.register(ProgressoPorLinguagem)
