from django.urls import path
from .views import mapa_mundi, conversar_com_npc

urlpatterns = [
    path('mapa/', mapa_mundi, name='mapa_mundi'),
    path('npc/<int:npc_id>/', conversar_com_npc, name='conversar_npc'),
]
