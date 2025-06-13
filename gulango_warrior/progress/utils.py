"""Utility functions for the progress app."""

from __future__ import annotations

from datetime import date
from typing import Dict, Any, Optional

from .models import (
    Conquista,
    AvatarConquista,
    MissaoDiaria,
    UsuarioMissao,
)
from avatars.models import Avatar


def _avaliar_condicao(
    condicao: str,
    avatar: Avatar,
    contexto_extra: Optional[Dict[str, Any]] = None,
) -> bool:
    """Avalia uma condição de desbloqueio simples.

    A condição deve ser uma expressão Python básica que pode usar os
    seguintes nomes de variável: ``nivel``, ``xp``, ``xp_total`` e ``moedas``.
    Valores adicionais podem ser passados via ``contexto_extra``.  Exemplo:
    ``"nivel >= 5"`` ou ``"xp_total >= 100"``.
    """
    if not condicao:
        return True

    contexto: Dict[str, Any] = {
        "nivel": avatar.nivel,
        "xp": avatar.xp_total,
        "xp_total": avatar.xp_total,
        "moedas": avatar.moedas,
    }
    if contexto_extra:
        contexto.update(contexto_extra)
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


def verificar_missoes_automaticas(
    usuario, contexto_extra: Optional[Dict[str, Any]] = None
) -> None:
    """Avalia e conclui automaticamente missões diárias para o usuário."""

    avatar = Avatar.objects.get(user=usuario)
    hoje = date.today()
    for missao in MissaoDiaria.objects.all():
        usuario_missao, _ = UsuarioMissao.objects.get_or_create(
            usuario=usuario, missao=missao, data=hoje
        )
        if usuario_missao.concluida:
            continue

        if _avaliar_condicao(missao.condicao, avatar, contexto_extra):
            avatar.ganhar_xp(missao.xp_recompensa)
            avatar.moedas += missao.moedas_recompensa
            avatar.save()
            usuario_missao.concluida = True
            usuario_missao.save()
