from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from avatars.models import Avatar
from .models import Item, CompraItem


@login_required
def loja_view(request):
    """Exibe os itens e processa a compra de um item."""
    avatar = Avatar.objects.get(user=request.user)
    itens = Item.objects.all()
    mensagem = request.session.pop("mensagem_loja", None)

    if request.method == "POST":
        item_id = request.POST.get("item_id")
        item = get_object_or_404(Item, pk=item_id)

        classe_ok = item.classe_restrita == "todas" or item.classe_restrita == avatar.classe
        moedas_ok = avatar.moedas >= item.preco

        if classe_ok and moedas_ok:
            avatar.moedas -= item.preco
            avatar.save()
            CompraItem.objects.create(avatar=avatar, item=item)
            request.session["mensagem_loja"] = "Item comprado com sucesso!"
        else:
            request.session["mensagem_loja"] = "Você não pode comprar este item."
        return redirect("loja_view")

    context = {
        "itens": itens,
        "avatar": avatar,
        "mensagem": mensagem,
    }
    return render(request, "marketplace/loja.html", context)
