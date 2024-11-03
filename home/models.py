from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    lote = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField()
    vencimento = models.DateField()
    setor_armazenamento = models.CharField(max_length=100)
    codigo_barra = models.CharField(max_length=100, unique=True)
