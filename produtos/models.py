# produtos/models.py

from django.db import models

class Produto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descricao = models.CharField(max_length=255)
    perecivel = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao