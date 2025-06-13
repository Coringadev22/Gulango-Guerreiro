from django.urls import path
from .views import (
    perfil_avatar,
    ranking_geral,
    destaque_conquistas,
    inventario_skins,
    loja_skins,
)

urlpatterns = [
    path('perfil/', perfil_avatar, name='perfil_avatar'),
    path('ranking/', ranking_geral, name='ranking_geral'),
    path('conquistas/', destaque_conquistas, name='destaque_conquistas'),
    path('inventario/', inventario_skins, name='inventario_skins'),
    path('loja/', loja_skins, name='loja_skins'),
]
