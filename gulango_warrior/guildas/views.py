from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import Guilda, MembroGuilda
from avatars.models import Avatar


@login_required
def perfil_guilda(request, guilda_id: int):
    """Exibe detalhes de uma guilda e de seus membros."""

    guilda = get_object_or_404(Guilda, pk=guilda_id)
    membros = (
        MembroGuilda.objects.filter(guilda=guilda)
        .select_related("usuario__avatar")
        .order_by("-usuario__avatar__xp_total")
    )

    membros_info = []
    xp_total = 0
    for membro in membros:
        avatar = getattr(membro.usuario, "avatar", None)
        xp = avatar.xp_total if avatar else 0
        membros_info.append({"membro": membro, "xp": xp})
        xp_total += xp

    context = {
        "guilda": guilda,
        "membros": membros_info,
        "xp_total": xp_total,
    }
    return render(request, "guildas/perfil_guilda.html", context)

