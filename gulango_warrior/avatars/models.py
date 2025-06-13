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

    def ganhar_xp(self, quantidade: int) -> None:
        """Incrementa o XP do avatar e dispara notificações."""

        from progress.utils import verificar_conquistas, enviar_notificacao

        nivel_anterior = self.nivel
        self.xp_total += quantidade
        while self.xp_total >= self.nivel * 100:
            self.nivel += 1
        self.save()

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
