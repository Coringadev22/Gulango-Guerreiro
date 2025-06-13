from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Course, Lesson, NPC, HistoricoDialogo
from .utils import gerar_resposta_ia
from progress.models import LessonProgress


@login_required
def mapa_mundi(request):
    """Exibe todos os cursos com o progresso do usuário."""
    cursos_info = []

    for curso in Course.objects.all():
        total_aulas = Lesson.objects.filter(course=curso).count()
        progresso_qs = LessonProgress.objects.filter(
            user=request.user, lesson__course=curso
        )

        concluidas = progresso_qs.filter(completed=True).count()

        if not progresso_qs.exists():
            status = "não iniciado"
        elif total_aulas > 0 and concluidas == total_aulas:
            status = "concluído"
        else:
            status = "em andamento"

        cursos_info.append(
            {
                "curso": curso,
                "status": status,
                "concluidas": concluidas,
                "total": total_aulas,
            }
        )

    context = {"cursos": cursos_info}
    return render(request, "courses/mapa_mundi.html", context)


@login_required
def conversar_com_npc(request, npc_id: int):
    """Exibe a conversa com um NPC e processa perguntas do usuário."""
    npc = get_object_or_404(NPC, pk=npc_id)
    resposta = None

    if request.method == "POST":
        pergunta = request.POST.get("pergunta", "")
        if npc.tipo == NPC.FIXO:
            resposta = npc.frase_inicial
        else:
            resposta = gerar_resposta_ia(pergunta, npc)

        HistoricoDialogo.objects.create(
            npc=npc,
            usuario=request.user,
            pergunta=pergunta,
            resposta=resposta,
        )

    context = {
        "npc": npc,
        "frase_inicial": npc.frase_inicial,
        "resposta": resposta,
    }
    return render(request, "courses/conversar_com_npc.html", context)

