from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Avatar


@login_required
def perfil_avatar(request):
    """Exibe os dados do avatar do usuário logado."""
    avatar = Avatar.objects.get(user=request.user)
    context = {
        "avatar": avatar,
    }
    return render(request, "avatars/perfil.html", context)

