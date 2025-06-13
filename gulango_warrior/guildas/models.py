from django.db import models


class Guilda(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    brasao = models.ImageField(upload_to="brasoes/")
    lider = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.nome


class MembroGuilda(models.Model):
    """Relaciona um usuario a uma :class:`Guilda`."""

    CARGO_LIDER = "líder"
    CARGO_OFICIAL = "oficial"
    CARGO_MEMBRO = "membro"

    CARGO_CHOICES = [
        (CARGO_LIDER, "líder"),
        (CARGO_OFICIAL, "oficial"),
        (CARGO_MEMBRO, "membro"),
    ]

    usuario = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    guilda = models.ForeignKey(Guilda, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES)
    data_entrada = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover - simples representacao
        return f"{self.usuario} - {self.guilda} ({self.cargo})"
