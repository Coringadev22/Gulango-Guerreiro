from django.db import models

# Create your models here.
class LessonProgress(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    lesson = models.ForeignKey('courses.Lesson', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)



class Conquista(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    icone = models.ImageField(upload_to='conquistas/')
    condicao = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
