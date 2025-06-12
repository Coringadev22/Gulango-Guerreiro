from django.urls import path
from .views import loja_view

urlpatterns = [
    path('loja/', loja_view, name='loja'),
]
