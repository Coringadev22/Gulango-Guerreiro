from django.urls import path
from .views import perfil_avatar, ranking_geral

urlpatterns = [
    path('perfil/', perfil_avatar, name='perfil_avatar'),
    path('ranking/', ranking_geral, name='ranking_geral'),
]
