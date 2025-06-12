from django.urls import path
from .views import perfil_avatar

urlpatterns = [
    path('perfil/', perfil_avatar, name='perfil_avatar'),
]
