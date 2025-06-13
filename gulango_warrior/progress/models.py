from django.db import models
from .validators import validate_condicao


# Create your models here.
class LessonProgress(models.Model):
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    lesson = models.ForeignKey("courses.Lesson", on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)


class Conquista(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    icone = models.ImageField(upload_to="conquistas/")
    condicao = models.CharField(max_length=100, validators=[validate_condicao])

    def __str__(self):
        return self.nome

    def avatarconquista_count(self) -> int:
        """Return how many avatars have unlocked this achievement."""
        return self.avatarconquista_set.count()


class AvatarConquista(models.Model):
    avatar = models.ForeignKey("avatars.Avatar", on_delete=models.CASCADE)
    conquista = models.ForeignKey(Conquista, on_delete=models.CASCADE)
    data_desbloqueio = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.avatar} - {self.conquista}"


class MissaoDiaria(models.Model):
    """Representa uma missão diária que os usuários podem cumprir."""

    descricao = models.CharField(max_length=255)
    xp_recompensa = models.IntegerField()
    moedas_recompensa = models.IntegerField()
    condicao = models.CharField(max_length=100, validators=[validate_condicao])

    def __str__(self) -> str:  # pragma: no cover - simples representacao
        return self.descricao


class UsuarioMissao(models.Model):
    """Relaciona um usuário com uma missão diária em uma data específica."""

    usuario = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    missao = models.ForeignKey(MissaoDiaria, on_delete=models.CASCADE)
    concluida = models.BooleanField(default=False)
    data = models.DateField()

    def __str__(self) -> str:  # pragma: no cover - simples representacao
        return f"{self.usuario} - {self.missao} ({self.data})"


class Notificacao(models.Model):
    usuario = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    mensagem = models.TextField()

    TIPO_CONQUISTA = "conquista"
    TIPO_XP = "xp"
    TIPO_NIVEL = "nivel"
    TIPO_SISTEMA = "sistema"
    TIPO_CHOICES = [
        (TIPO_CONQUISTA, "conquista"),
        (TIPO_XP, "xp"),
        (TIPO_NIVEL, "nivel"),
        (TIPO_SISTEMA, "sistema"),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    lida = models.BooleanField(default=False)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.titulo
