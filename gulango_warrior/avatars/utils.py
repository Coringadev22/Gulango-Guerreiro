"""Utility functions for the avatars app."""

from django.shortcuts import get_object_or_404

from accounts.models import CustomUser
from .models import SkinVisual, SkinUsuario


def trocar_skin(usuario: CustomUser, tipo: str, nova_skin_id: int) -> None:
    """Altera a skin em uso para ``usuario``.

    Todas as skins do mesmo ``tipo`` ficam com ``em_uso=False`` e a
    skin indicada por ``nova_skin_id`` passa a ter ``em_uso=True``.
    Caso o usuário ainda n\u00e3o possua a skin informada, o registro \u00e9
    criado automaticamente.
    """

    nova_skin = get_object_or_404(SkinVisual, id=nova_skin_id, tipo=tipo)

    # Desativa qualquer skin do mesmo tipo que esteja em uso
    SkinUsuario.objects.filter(usuario=usuario, skin__tipo=tipo, em_uso=True).update(
        em_uso=False
    )

    # Ativa (ou cria) a nova skin
    skin_usuario, _ = SkinUsuario.objects.get_or_create(
        usuario=usuario, skin=nova_skin, defaults={"em_uso": True}
    )
    if not skin_usuario.em_uso:
        skin_usuario.em_uso = True
        skin_usuario.save()
