from django.urls import path
from .views import mapa_mundi

urlpatterns = [
    path('mapa/', mapa_mundi, name='mapa_mundi'),
]
