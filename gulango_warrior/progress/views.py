from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from avatars.models import Avatar
from .models import MissaoDiaria, UsuarioMissao
from .utils import _avaliar_condicao


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
            avatar.ganhar_xp(missao.xp_recompensa)
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
