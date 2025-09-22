from django.urls import path
from . import views

urlpatterns = [
    path('', views.produtos_list, name='produtos_list'),
    path('<int:id_produto>/', views.produto_detail, name='produto_detail'),
]