from django.contrib import admin
from .models import (
    LessonProgress,
    Conquista,
    AvatarConquista,
    MissaoDiaria,
    UsuarioMissao,
)

admin.site.register(LessonProgress)
@admin.register(Conquista)
class ConquistaAdmin(admin.ModelAdmin):
    list_display = ("nome", "condicao", "avatarconquista_count")
admin.site.register(AvatarConquista)
admin.site.register(MissaoDiaria)
admin.site.register(UsuarioMissao)
