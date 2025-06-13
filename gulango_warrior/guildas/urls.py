from django.urls import path
from .views import criar_guilda
from .views import perfil_guilda

urlpatterns = [
    path('perfil/<int:guilda_id>/', perfil_guilda, name='perfil_guilda'),
    path('criar/', criar_guilda, name='criar_guilda'),
]
