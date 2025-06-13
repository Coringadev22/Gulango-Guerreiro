from django.db import models
from accounts.models import CustomUser
from progress.models import Notificacao


class Avatar(models.Model):
    CLASSE_CHOICES = [
        ("mago", "Mago"),
        ("guerreiro", "Guerreiro"),
        ("arqueiro", "Arqueiro"),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    classe = models.CharField(max_length=20, choices=CLASSE_CHOICES, default="guerreiro")
    nivel = models.IntegerField(default=1)
    xp_total = models.IntegerField(default=0)
    moedas = models.IntegerField(default=0)

    def ganhar_xp(self, quantidade: int, linguagem: str | None = None) -> None:
        """Incrementa o XP do avatar, atualizando conquistas e progresso.

        Se ``linguagem`` for fornecida, o progresso do usuário na
        :class:`~progress.models.ProgressoPorLinguagem` correspondente é
        criado ou atualizado com o XP recebido.
        """

        from progress.utils import (
            verificar_conquistas,
            enviar_notificacao,
            atualizar_progresso_linguagem,
        )

        nivel_anterior = self.nivel
        self.xp_total += quantidade
        while self.xp_total >= self.nivel * 100:
            self.nivel += 1
        self.save()

        if linguagem:
            atualizar_progresso_linguagem(self.user, linguagem, quantidade)

        enviar_notificacao(
            self.user,
            "Ganho de XP",
            f"Você ganhou +{quantidade} XP por concluir uma missão!",
            Notificacao.TIPO_XP,
        )

        if self.nivel > nivel_anterior:
            enviar_notificacao(
                self.user,
                "Subiu de nível",
                f"Parabéns! Você alcançou o nível {self.nivel}!",
                Notificacao.TIPO_NIVEL,
            )

        verificar_conquistas(self)

    def __str__(self) -> str:
        return f"{self.user.username} - Nível {self.nivel}"


class SkinVisual(models.Model):
    """Representa elementos visuais personalizáveis disponíveis no jogo."""

    TIPO_AVATAR = "avatar"
    TIPO_FUNDO = "fundo_perfil"
    TIPO_MOLDURA = "moldura"
    TIPO_BRASAO = "brasao"

    TIPO_CHOICES = [
        (TIPO_AVATAR, "avatar"),
        (TIPO_FUNDO, "fundo_perfil"),
        (TIPO_MOLDURA, "moldura"),
        (TIPO_BRASAO, "brasao"),
    ]

    CLASSE_CHOICES = [
        ("mago", "Mago"),
        ("guerreiro", "Guerreiro"),
        ("arqueiro", "Arqueiro"),
        ("todas", "Todas"),
    ]

    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    imagem = models.ImageField(upload_to="skins/")
    preco_moedas = models.IntegerField()
    classe_restrita = models.CharField(
        max_length=20, choices=CLASSE_CHOICES, default="todas"
    )

    def __str__(self) -> str:  # pragma: no cover - simples representacao
        return self.nome
