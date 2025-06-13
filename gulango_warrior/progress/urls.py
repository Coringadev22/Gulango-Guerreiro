from django.urls import path
from .views import missoes_do_dia

urlpatterns = [
    path('missoes/', missoes_do_dia, name='missoes_diarias'),
]
