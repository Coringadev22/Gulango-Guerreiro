from django.contrib import admin
from .models import Course, Lesson, NPC, HistoricoDialogo


class HistoricoDialogoAdmin(admin.ModelAdmin):
    list_display = ("npc", "usuario", "pergunta", "resposta", "data")
    search_fields = ("usuario__username", "npc__nome")
    ordering = ["-data"]

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(NPC)
admin.site.register(HistoricoDialogo, HistoricoDialogoAdmin)
