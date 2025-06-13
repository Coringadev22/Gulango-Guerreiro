from django.urls import path

from .views import perfil_guilda

urlpatterns = [
    path('perfil/<int:guilda_id>/', perfil_guilda, name='perfil_guilda'),
]
