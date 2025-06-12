from django.db import models
from accounts.models import CustomUser


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
        """Incrementa o XP do avatar e verifica conquistas."""

        self.xp_total += quantidade
        while self.xp_total >= self.nivel * 100:
            self.nivel += 1
        self.save()

        # Importação tardia para evitar dependência circular
        from progress.utils import verificar_conquistas

        verificar_conquistas(self)

    def __str__(self) -> str:
        return f"{self.user.username} - Nível {self.nivel}"
