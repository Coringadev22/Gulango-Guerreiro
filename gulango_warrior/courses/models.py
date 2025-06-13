from django.db import models

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

    REGIAO_FLORESTA_GO = "floresta_de_go"
    REGIAO_FORTALEZA_RUSTICA = "fortaleza_rustica"
    REGIAO_PLANICIES_JULIANAS = "planicies_julianas"

    REGIAO_CHOICES = [
        (REGIAO_FLORESTA_GO, "floresta_de_go"),
        (REGIAO_FORTALEZA_RUSTICA, "fortaleza_rustica"),
        (REGIAO_PLANICIES_JULIANAS, "planicies_julianas"),
    ]

    regiao = models.CharField(
        max_length=20,
        choices=REGIAO_CHOICES,
        default=REGIAO_FLORESTA_GO,
    )
    created_at = models.DateTimeField(auto_now_add=True)

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    order = models.PositiveIntegerField()


class NPC(models.Model):
    FIXO = "fixo"
    IA = "ia"

    TIPO_CHOICES = [
        (FIXO, "fixo"),
        (IA, "ia"),
    ]

    nome = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to="npcs/")
    curso = models.ForeignKey(Course, on_delete=models.CASCADE)
    frase_inicial = models.TextField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default=FIXO)

    def __str__(self) -> str:
        return self.nome
