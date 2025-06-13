"""Utility functions for the progress app."""

from __future__ import annotations

from datetime import date
from typing import Dict, Any, Optional
import ast
import operator
import os

try:
    import openai
except Exception:  # openai not installed
    openai = None

from .models import (
    Conquista,
    AvatarConquista,
    MissaoDiaria,
    UsuarioMissao,
    LessonProgress,
    Notificacao,
)
from avatars.models import Avatar


_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
}

_CMP_OPS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
}


def enviar_notificacao(usuario, titulo: str, mensagem: str, tipo: str) -> None:
    """Cria uma :class:`~progress.models.Notificacao` para o usuário."""

    Notificacao.objects.create(
        usuario=usuario,
        titulo=titulo,
        mensagem=mensagem,
        tipo=tipo,
    )


def _safe_eval(expr: str, variables: Dict[str, Any]) -> Any:
    """Avalia uma expressão usando apenas operações seguras."""

    def _eval(node: ast.AST) -> Any:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float, bool)):
                return node.value
            raise ValueError("Valor literal não permitido")
        if isinstance(node, ast.Name):
            if node.id in variables:
                return variables[node.id]
            raise ValueError(f"Variável não permitida: {node.id}")
        if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
            return _BIN_OPS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.BoolOp):
            values = [_eval(v) for v in node.values]
            if isinstance(node.op, ast.And):
                return all(values)
            if isinstance(node.op, ast.Or):
                return any(values)
        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.Not):
                return not _eval(node.operand)
            if isinstance(node.op, ast.USub):
                return -_eval(node.operand)
        if isinstance(node, ast.Compare):
            left = _eval(node.left)
            for op, comparator in zip(node.ops, node.comparators):
                if type(op) not in _CMP_OPS:
                    raise ValueError("Operação de comparação não permitida")
                right = _eval(comparator)
                if not _CMP_OPS[type(op)](left, right):
                    return False
                left = right
            return True
        raise ValueError("Expressão não suportada")

    tree = ast.parse(expr, mode="eval")
    return _eval(tree)


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
        return bool(_safe_eval(condicao, contexto))
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
            enviar_notificacao(
                avatar.user,
                "Conquista desbloqueada",
                f"Você desbloqueou a conquista {conquista.nome}!",
                Notificacao.TIPO_CONQUISTA,
            )


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


def gerar_feedback_ia(avatar: Avatar) -> str:
    """Gera uma mensagem de feedback em tom medieval via OpenAI.

    A função coleta informações do avatar e retorna elogios, dicas e
    orientações para a próxima jornada. Se a API da OpenAI não estiver
    disponível ou ocorrer qualquer erro, uma resposta padrão é retornada.
    """

    if openai is None:
        return "Não posso falar agora, jovem aventureiro."

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "API key não configurada."

    openai.api_key = api_key

    conquistas = AvatarConquista.objects.filter(avatar=avatar).select_related(
        "conquista"
    )
    nomes_conquistas = [ac.conquista.nome for ac in conquistas]

    exercicios_resolvidos = LessonProgress.objects.filter(
        user=avatar.user, completed=True
    ).count()

    system_prompt = (
        "Você é um mestre medieval que orienta jovens heróis em sua jornada. "
        "Elogie seus feitos, ofereça dicas breves e indique o caminho para a "
        "próxima aventura. Responda em português."
    )
    user_content = (
        f"XP atual: {avatar.xp_total}\n"
        f"Exercícios resolvidos: {exercicios_resolvidos}\n"
        f"Conquistas: {', '.join(nomes_conquistas) if nomes_conquistas else 'nenhuma'}"
    )

    try:
        resposta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        )
        return resposta.choices[0].message.content.strip()
    except Exception:
        return "O oráculo silenciou-se por ora. Volte mais tarde."
