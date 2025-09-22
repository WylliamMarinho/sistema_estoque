# estoque/models.py

from django.db import models
from produtos.models import Produto

class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='entradas_estoque')
    data_entrada = models.DateField()
    quantidade_entrada = models.IntegerField()
    valor_compra = models.DecimalField(max_digits=10, decimal_places=2)
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_vendida = models.IntegerField(default=0)
    data_vencimento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Entrada de {self.quantidade_entrada} de {self.produto.descricao}"