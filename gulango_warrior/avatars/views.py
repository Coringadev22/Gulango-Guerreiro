from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Avatar
from progress.models import AvatarConquista


@login_required
def perfil_avatar(request):
    """Exibe os dados do avatar do usuário logado."""
    avatar = Avatar.objects.get(user=request.user)
    conquistas = (
        AvatarConquista.objects.filter(avatar=avatar)
        .select_related("conquista")
        .order_by("data_desbloqueio")
    )
    context = {
        "avatar": avatar,
        "conquistas": conquistas,
    }
    return render(request, "avatars/perfil.html", context)

