
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

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Guilda, MembroGuilda


@login_required
def criar_guilda(request):
    """Permite que o usuário crie uma guilda se não fizer parte de nenhuma."""

    ja_membro = MembroGuilda.objects.filter(usuario=request.user).exists()
    mensagem = request.session.pop("mensagem_guilda", None)

    if ja_membro:
        return render(request, "guildas/criar_guilda.html", {"erro": "Você já pertence a uma guilda.", "mensagem": mensagem})

    if request.method == "POST":
        nome = request.POST.get("nome", "")
        descricao = request.POST.get("descricao", "")
        brasao = request.FILES.get("brasao")

        guilda = Guilda.objects.create(
            nome=nome,
            descricao=descricao,
            brasao=brasao,
            lider=request.user,
        )
        MembroGuilda.objects.create(
            usuario=request.user,
            guilda=guilda,
            cargo=MembroGuilda.CARGO_LIDER,
        )
        request.session["mensagem_guilda"] = "Guilda criada com sucesso!"
        return redirect("criar_guilda")

    return render(request, "guildas/criar_guilda.html", {"mensagem": mensagem})

