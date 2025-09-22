from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes_list, name='clientes_list'),
    path('<int:id_cliente>/', views.cliente_detail, name='cliente_detail'),
]