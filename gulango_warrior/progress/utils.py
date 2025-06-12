"""Utility functions for the progress app."""

from __future__ import annotations

from typing import Dict, Any

from .models import Conquista, AvatarConquista
from avatars.models import Avatar


def _avaliar_condicao(condicao: str, avatar: Avatar) -> bool:
    """Avalia uma condição de desbloqueio simples.

    A condição deve ser uma expressão Python básica que pode usar os
    seguintes nomes de variável: ``nivel``, ``xp``, ``xp_total`` e ``moedas``.
    Exemplo: ``"nivel >= 5"`` ou ``"xp_total >= 100"``.
    """
    if not condicao:
        return False

    contexto: Dict[str, Any] = {
        "nivel": avatar.nivel,
        "xp": avatar.xp_total,
        "xp_total": avatar.xp_total,
        "moedas": avatar.moedas,
    }
    try:
        return bool(eval(condicao, {}, contexto))
    except Exception:
        # Se a condição não puder ser avaliada, consideramos que não foi atendida
        return False


def verificar_conquistas(avatar: Avatar) -> None:
    """Verifica e concede conquistas para o avatar informado.

    Para cada :class:`~progress.models.Conquista` existente, a função verifica
    se o avatar já possui a conquista. Caso não possua e a condição seja
    satisfeita, é criado um registro :class:`~progress.models.AvatarConquista`.
    """
    conquistas = Conquista.objects.all()
    for conquista in conquistas:
        ja_possui = AvatarConquista.objects.filter(
            avatar=avatar, conquista=conquista
        ).exists()
        if ja_possui:
            continue

        if _avaliar_condicao(conquista.condicao, avatar):
            AvatarConquista.objects.create(avatar=avatar, conquista=conquista)
