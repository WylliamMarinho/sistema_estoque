# sistema_estoque/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/clientes/', include('clientes.urls')),
    path('v1/produtos/', include('produtos.urls')),
    path('v1/estoque/', include('estoque.urls')),
    path('v1/venda/', include('vendas.urls')),
    path('v1/relatorio/', include('relatorios.urls')),
]