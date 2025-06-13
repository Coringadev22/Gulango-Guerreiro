from django.urls import path
from .views import criar_guilda

urlpatterns = [
    path('criar/', criar_guilda, name='criar_guilda'),
]
