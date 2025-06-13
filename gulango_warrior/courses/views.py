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

