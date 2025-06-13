from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from progress.models import AvatarConquista

from .models import Avatar, SkinUsuario


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


@login_required
def ranking_geral(request):
    """Exibe o ranking geral dos avatares."""

    avatares = Avatar.objects.all().order_by("-xp_total")[:10]

    context = {
        "avatares": avatares,
    }
    return render(request, "avatars/ranking.html", context)


@login_required
def destaque_conquistas(request):
    """Exibe os avatares com mais conquistas desbloqueadas."""

    avatares = (
        Avatar.objects.annotate(qtd_conquistas=Count("avatarconquista"))
        .prefetch_related("avatarconquista_set__conquista")
        .order_by("-qtd_conquistas")[:5]
    )

    context = {
        "avatares": avatares,
    }
    return render(request, "avatars/conquistas_ranking.html", context)


@login_required
def inventario_skins(request):
    """Lista as skins possuídas pelo usuário e indica qual está em uso."""

    skins_usuario = (
        SkinUsuario.objects.filter(usuario=request.user)
        .select_related("skin")
        .order_by("skin__nome")
    )

    context = {"skins_usuario": skins_usuario}
    return render(request, "avatars/inventario_skins.html", context)

