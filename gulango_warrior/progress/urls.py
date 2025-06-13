from django.urls import path
from .views import missoes_do_dia, feedback_personalizado

urlpatterns = [
    path('missoes/', missoes_do_dia, name='missoes_diarias'),
    path('feedback/', feedback_personalizado, name='feedback_personalizado'),
]
