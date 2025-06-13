from django.contrib import admin
from .models import (
    LessonProgress,
    Conquista,
    AvatarConquista,
    MissaoDiaria,
    UsuarioMissao,
)

admin.site.register(LessonProgress)
admin.site.register(Conquista)
admin.site.register(AvatarConquista)
admin.site.register(MissaoDiaria)
admin.site.register(UsuarioMissao)
