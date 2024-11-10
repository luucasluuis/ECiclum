from django.db import models

class Categoria(models.Model):
    nome_categoria = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome_categoria


class Fornecedor(models.Model):
    nome_fornecedor = models.CharField(max_length=100)
    contato = models.CharField(max_length=100, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    endereco = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_fornecedor


class Produto(models.Model):
    nome_produto = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, null=True, blank=True)  # permite null temporariamente
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.DO_NOTHING)
    codigo_barras = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True)
    unidade_medida = models.CharField(max_length=20)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome_produto} - {self.codigo_barras}"


class Lote(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    quantidade = models.PositiveIntegerField()
    data_recebimento = models.DateField()
    data_validade = models.DateField()
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=15,
        choices=[
            ('ativo', 'Ativo'),
            ('em promoção', 'Em Promoção'),
            ('vencido', 'Vencido')
        ]
    )

    def __str__(self):
        return f"Lote de {self.produto.nome_produto} - Vencimento: {self.data_validade}"


class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    lote = models.ForeignKey(Lote, on_delete=models.DO_NOTHING)
    tipo_movimento = models.CharField(
        max_length=10,
        choices=[('entrada', 'Entrada'), ('saida', 'Saída'), ('ajuste', 'Ajuste')]
    )
    quantidade = models.IntegerField()
    data_movimento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_movimento} - {self.produto.nome_produto} ({self.quantidade})"


class Promocao(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.DO_NOTHING)
    tipo_promocao = models.CharField(
        max_length=10,
        choices=[('desconto', 'Desconto'), ('combo', 'Combo')]
    )
    valor_desconto = models.DecimalField(max_digits=5, decimal_places=2)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"Promoção de {self.tipo_promocao} - Lote: {self.lote}"


class PrevisaoDemanda(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    data_previsao = models.DateField()
    quantidade_prevista = models.PositiveIntegerField()
    modelo_ia = models.CharField(max_length=50, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Previsão para {self.produto.nome_produto} - {self.data_previsao}"


class Alerta(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.DO_NOTHING)
    mensagem = models.TextField()
    data_alerta = models.DateTimeField(auto_now_add=True)
    resolvido = models.BooleanField(default=False)

    def __str__(self):
        return f"Alerta para Lote {self.lote} - {self.data_alerta}"
