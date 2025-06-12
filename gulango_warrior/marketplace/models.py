from django.db import models


class Item(models.Model):
    CLASSE_CHOICES = [
        ("mago", "Mago"),
        ("guerreiro", "Guerreiro"),
        ("arqueiro", "Arqueiro"),
        ("todas", "Todas"),
    ]

    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.IntegerField()
    imagem = models.ImageField(upload_to="itens/")
    classe_restrita = models.CharField(max_length=20, choices=CLASSE_CHOICES, default="todas")

    def __str__(self) -> str:
        return self.nome
