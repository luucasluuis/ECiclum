# estoque/forms.py
from django import forms
from .models import Produto, Fornecedor, Categoria, Lote

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'fornecedor', 'codigo_barras', 'descricao', 'unidade_medida', 'preco_custo', 'preco_venda', 'ativo']

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'contato', 'telefone', 'email', 'endereco']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']

class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['produto', 'quantidade', 'data_recebimento', 'data_validade', 'preco_custo', 'status']
