import ast
from django.core.exceptions import ValidationError

ALLOWED_NAMES = {"nivel", "xp", "xp_total", "moedas"}
ALLOWED_NODES = (
    ast.Expression,
    ast.BoolOp,
    ast.BinOp,
    ast.UnaryOp,
    ast.Compare,
    ast.Name,
    ast.Load,
    ast.Constant,
    ast.And,
    ast.Or,
    ast.Not,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.USub,
)


def validate_condicao(value: str) -> None:
    """Valida a expressão de condição para missões e conquistas."""
    try:
        tree = ast.parse(value, mode="eval")
    except Exception as exc:
        raise ValidationError("Expressão inválida") from exc

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            raise ValidationError("Chamadas de função não são permitidas")
        if isinstance(node, ast.Name) and node.id not in ALLOWED_NAMES:
            raise ValidationError(f"Variável não permitida: {node.id}")
        if not isinstance(node, ALLOWED_NODES):
            raise ValidationError("Expressão contém operações não permitidas")
