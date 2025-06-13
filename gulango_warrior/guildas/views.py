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
