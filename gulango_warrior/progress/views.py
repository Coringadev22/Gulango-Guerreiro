from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from avatars.models import Avatar
from .models import (
    MissaoDiaria,
    UsuarioMissao,
    Notificacao,
    AvatarConquista,
    ProgressoPorLinguagem,
    LessonProgress,
)
from .utils import _avaliar_condicao, gerar_feedback_ia


@login_required
def missoes_do_dia(request):
    """Exibe as missões diárias e processa sua conclusão."""
    avatar = Avatar.objects.get(user=request.user)
    hoje = date.today()
    mensagem = request.session.pop("mensagem_missoes", None)

    if request.method == "POST":
        missao_id = request.POST.get("missao_id")
        missao = get_object_or_404(MissaoDiaria, pk=missao_id)
        usuario_missao, _ = UsuarioMissao.objects.get_or_create(
            usuario=request.user, missao=missao, data=hoje
        )
        if not usuario_missao.concluida and _avaliar_condicao(missao.condicao, avatar):
            linguagem = request.POST.get("linguagem")
            avatar.ganhar_xp(missao.xp_recompensa, linguagem=linguagem)
            avatar.moedas += missao.moedas_recompensa
            avatar.save()
            usuario_missao.concluida = True
            usuario_missao.save()
            request.session["mensagem_missoes"] = "Missão concluída!"
        return redirect("missoes_diarias")

    missoes_info = []
    for missao in MissaoDiaria.objects.all():
        usuario_missao = UsuarioMissao.objects.filter(
            usuario=request.user, missao=missao, data=hoje
        ).first()
        concluida = usuario_missao.concluida if usuario_missao else False
        condicao_ok = _avaliar_condicao(missao.condicao, avatar)
        missoes_info.append(
            {"missao": missao, "concluida": concluida, "condicao_ok": condicao_ok}
        )

    context = {"missoes_info": missoes_info, "mensagem": mensagem}
    return render(request, "progress/missoes.html", context)


@login_required
def feedback_personalizado(request):
    """Gera e exibe um feedback personalizado para o usuário logado."""

    avatar = Avatar.objects.get(user=request.user)
    mensagem = gerar_feedback_ia(avatar)

    context = {"mensagem": mensagem, "avatar": avatar}
    return render(request, "progress/feedback.html", context)


@login_required
def notificacoes_usuario(request):
    """Lista as notificações do usuário logado e permite marcá-las como lidas."""

    if request.method == "POST":
        notif_id = request.POST.get("notificacao_id")
        notificacao = get_object_or_404(Notificacao, pk=notif_id, usuario=request.user)
        notificacao.lida = True
        notificacao.save()
        return redirect("notificacoes_usuario")

    notificacoes = Notificacao.objects.filter(usuario=request.user).order_by("-data")
    context = {"notificacoes": notificacoes}
    return render(request, "notificacoes/lista.html", context)


@login_required
def painel_linguagens(request):
    """Exibe o progresso do usuário em cada linguagem."""
    avatar = Avatar.objects.get(user=request.user)
    conquistas = AvatarConquista.objects.filter(avatar=avatar).select_related(
        "conquista"
    )

    linguagens_info = []
    for codigo, nome in ProgressoPorLinguagem.LINGUAGEM_CHOICES:
        progresso = ProgressoPorLinguagem.objects.filter(
            usuario=request.user, linguagem=codigo
        ).first()
        xp_total = progresso.xp_total if progresso else 0
        nivel = progresso.nivel if progresso else 1
        xp_atual = xp_total - (nivel - 1) * 100
        xp_proximo = nivel * 100
        conquistas_lang = conquistas.filter(conquista__nome__icontains=nome)
        linguagens_info.append(
            {
                "codigo": codigo,
                "nome": nome,
                "nivel": nivel,
                "xp_atual": xp_atual,
                "xp_proximo": xp_proximo,
                "conquistas": conquistas_lang,
            }
        )

    context = {"linguagens": linguagens_info}
    return render(request, "progress/painel_linguagens.html", context)

@login_required
def emitir_certificado(request, curso_id: int):
    """Emite um certificado caso o curso esteja concluído."""
    from courses.models import Course, Lesson
    from .models import Certificado
    from .utils import gerar_certificado_pdf

    curso = get_object_or_404(Course, pk=curso_id)
    total = Lesson.objects.filter(course=curso).count()
    concluidas = LessonProgress.objects.filter(
        user=request.user, lesson__course=curso, completed=True
    ).count()

    if total == 0 or concluidas < total:
        return redirect('mapa_mundi')

    certificado = Certificado.objects.filter(usuario=request.user, curso=curso).first()
    if not certificado:
        certificado = gerar_certificado_pdf(request.user, curso)

    return redirect('ver_certificado', certificado_id=certificado.id)


@login_required
def ver_certificado(request, certificado_id: int):
    """Exibe uma página com link para download do certificado."""
    from .models import Certificado

    certificado = get_object_or_404(
        Certificado, pk=certificado_id, usuario=request.user
    )
    context = {'certificado': certificado}
    return render(request, 'progress/ver_certificado.html', context)
