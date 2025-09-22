from django.urls import path
from . import views

urlpatterns = [
    path('', views.registrar_venda, name='registrar_venda'),
]