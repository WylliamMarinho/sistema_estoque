from django.urls import path
from . import views

urlpatterns = [
    path('produto/<int:produto_id>/', views.relatorio_produto, name='relatorio_produto'),
]