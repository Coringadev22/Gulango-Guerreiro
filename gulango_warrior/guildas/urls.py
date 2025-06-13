from django.urls import path
from .views import criar_guilda, perfil_guilda, ranking_guildas

urlpatterns = [
    path('perfil/<int:guilda_id>/', perfil_guilda, name='perfil_guilda'),
    path('criar/', criar_guilda, name='criar_guilda'),
    path('ranking/', ranking_guildas, name='ranking_guildas'),
