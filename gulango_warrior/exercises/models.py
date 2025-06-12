from django.db import models

# Create your models here.
class Exercise(models.Model):
    lesson = models.ForeignKey('courses.Lesson', on_delete=models.CASCADE)
    question_text = models.TextField()
    correct_answer = models.TextField()
    answer_type = models.CharField(max_length=20, choices=[('code', 'Code'), ('quiz', 'Quiz')])
    xp_recompensa = models.IntegerField(default=10)
    