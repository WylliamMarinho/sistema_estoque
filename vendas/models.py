# vendas/models.py

from django.db import models
from clientes.models import Cliente
from estoque.models import Estoque

class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venda #{self.id} em {self.data.strftime('%d/%m/%Y')}"

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    estoque = models.ForeignKey(Estoque, on_delete=models.SET_NULL, null=True, blank=True)
    quantidade = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade} unidades de {self.estoque.produto.descricao}"