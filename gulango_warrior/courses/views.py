from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Course, Lesson
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

        iniciou = progresso_qs.exists()
        concluidas = progresso_qs.filter(completed=True).count()
        concluido = total_aulas > 0 and concluidas == total_aulas

        cursos_info.append(
            {
                "curso": curso,
                "iniciado": iniciou,
                "concluido": concluido,
                "concluidas": concluidas,
                "total": total_aulas,
            }
        )

    context = {"cursos": cursos_info}
    return render(request, "courses/mapa_mundi.html", context)

