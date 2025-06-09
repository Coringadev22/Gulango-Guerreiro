from django.urls import path
from .views import code_executor

urlpatterns = [
    path('code/', code_executor, name='code_executor'),
]
