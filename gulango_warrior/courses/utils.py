import os
from .models import NPC

try:
    import openai
except Exception:  # openai not installed
    openai = None


def gerar_resposta_ia(pergunta: str, npc: NPC) -> str:
    """Gera uma resposta usando a API da OpenAI.

    Caso a chave de API não esteja configurada ou ocorra algum erro, uma
    mensagem padrão é retornada.
    """
    if openai is None:
        return "Desculpe, não foi possível gerar a resposta."

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "API key não configurada."

    openai.api_key = api_key
    prompt = f"{npc.nome} diz:"

    try:
        resposta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": pergunta},
            ],
        )
        return resposta.choices[0].message.content.strip()
    except Exception:
        return "Desculpe, não consegui responder agora."


def gerar_resposta_npc(nome_npc: str, pergunta: str) -> str:
    """Gera uma resposta com tom medieval para o aluno.

    A resposta é produzida pela API da OpenAI. Caso a chave de API
    não esteja configurada ou ocorra algum erro, uma mensagem padrão é
    retornada.
    """
    if openai is None:
        return "Desculpe, não foi possível gerar a resposta."

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "API key não configurada."

    openai.api_key = api_key
    system_prompt = (
        f"Você é {nome_npc}, um sábio mestre de magia de um reino medieval. "
        "Responda de maneira breve e em tom medieval às perguntas dos alunos."
    )

    try:
        resposta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": pergunta},
            ],
        )
        return resposta.choices[0].message.content.strip()
    except Exception:
        return "Desculpe, não consegui responder agora."
