from django.db import models


class Guilda(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    brasao = models.ImageField(upload_to="brasoes/")
    lider = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.nome
