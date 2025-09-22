# clientes/models.py

from django.db import models

class Cliente(models.Model):
    cpf = models.CharField(max_length=14, unique=True)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome