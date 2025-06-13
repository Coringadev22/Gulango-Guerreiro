"""Utility functions for the avatars app."""

from .models import Avatar, SkinVisual, SkinUsuario
from accounts.models import CustomUser


def comprar_skin(usuario: CustomUser, skin: SkinVisual) -> bool:
    """Compra uma ``skin`` para ``usuario`` se houver moedas suficientes.

    Deduz o valor da skin do avatar, adiciona um registro ``SkinUsuario`` e
    define ``em_uso`` caso seja a primeira skin desse tipo para o usuário.

    Retorna ``True`` em caso de sucesso, ``False`` caso o usuário não tenha
    moedas suficientes.
    """

    avatar = Avatar.objects.get(user=usuario)
    if avatar.moedas < skin.preco_moedas:
        return False

    avatar.moedas -= skin.preco_moedas
    avatar.save()

    primeira = not SkinUsuario.objects.filter(
        usuario=usuario, skin__tipo=skin.tipo
    ).exists()

    SkinUsuario.objects.create(usuario=usuario, skin=skin, em_uso=primeira)
    return True
