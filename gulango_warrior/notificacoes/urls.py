from django.urls import path
from progress.views import notificacoes_usuario

urlpatterns = [
    path('minhas/', notificacoes_usuario, name='notificacoes_usuario'),
]

