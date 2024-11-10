from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .models import Produto, Fornecedor, Categoria, Lote
from django.db.models import Q
from django.db.models import Min
from .forms import ProdutoForm, FornecedorForm, CategoriaForm, LoteForm
from django.urls import reverse_lazy
from .service import gerar_insights

# Página inicial com login obrigatório
#removi a necessidade de login das views:
#para add login: class HomeView(TemplateView):
class HomeView(TemplateView):
    template_name = 'home/home.html'

class EstoqueView(TemplateView):
    template_name='home/estoque_list.html'

# Saída de estoque
class SaidaView(TemplateView):
    template_name = 'home/saida.html'

# Leitura de QR Code
class LerQRCodeView(TemplateView):
    template_name = 'home/leitura_qrcode.html'

# Página de erro 404
def custom_404(request, exception):
    return render(request, 'home/dashboard/404.html', status=404)

# Lista de produtos com paginação e filtragem
class ListaProdutosView(ListView):
    model = Produto
    template_name = 'home/dashboard/tables.html'
    context_object_name = 'page_obj'
    paginate_by = 10
    ordering = ['vencimento']

class ProdutoListView(ListView):
    model = Produto
    template_name = 'home/produtos_list.html'
    context_object_name = 'page_obj'
    paginate_by = 10  # Define o padrão de itens por página
    ordering = ['nome']  # Ordenação padrão

    def get_queryset(self):
        # Termo de pesquisa
        query = self.request.GET.get('termo', '')

        # Anotação da validade mais próxima e filtro
        produtos = Produto.objects.all().annotate(validade_mais_proxima=Min('lote__data_validade'))

        # Aplica o filtro de pesquisa, se houver um termo
        if query:
            produtos = produtos.filter(
                Q(nome_produto__icontains=query) | Q(codigo_barras__icontains=query)
            )

        return produtos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Adiciona variáveis ao contexto para uso no template
        context['query'] = self.request.GET.get('termo', '')
        context['itens_por_pagina'] = int(self.request.GET.get('itens_por_pagina', self.paginate_by))

        # Atualiza a paginação conforme o número de itens por página escolhido
        paginator = Paginator(self.get_queryset(), context['itens_por_pagina'])
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)

        return context

# Dashboard
class DashboardView(TemplateView):
    template_name = 'home/dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['service'] = gerar_insights()[:200]
        return context


# Gráficos
class ChartsView(TemplateView):
    template_name = 'home/dashboard/charts.html'

# Cartões (cards)
class CardsView(TemplateView):
    template_name = 'home/dashboard/cards.html'

class ProdutoCreateView(CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'home/produto_create.html'
    success_url = reverse_lazy('home:produtos_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fornecedor_form'] = FornecedorForm()
        context['categoria_form'] = CategoriaForm()
        context['lote_form'] = LoteForm()
        return context

    def post(self, request, *args, **kwargs):
        produto_form = ProdutoForm(request.POST)
        fornecedor_form = FornecedorForm(request.POST)
        categoria_form = CategoriaForm(request.POST)
        lote_form = LoteForm(request.POST)

        if produto_form.is_valid():
            # Salva o fornecedor, categoria ou lote se novos
            if fornecedor_form.is_valid() and fornecedor_form.cleaned_data['nome']:
                fornecedor = fornecedor_form.save()
                produto_form.instance.fornecedor = fornecedor

            if categoria_form.is_valid() and categoria_form.cleaned_data['nome']:
                categoria = categoria_form.save()
                produto_form.instance.categoria = categoria

            if lote_form.is_valid() and lote_form.cleaned_data['quantidade']:
                lote = lote_form.save()
                produto_form.instance.lote = lote

            # Salva o produto
            produto_form.save()
            return redirect(self.success_url)
        
        # Se algum formulário não for válido, renderize a página com erros
        return render(request, self.template_name, {
            'form': produto_form,
            'fornecedor_form': fornecedor_form,
            'categoria_form': categoria_form,
            'lote_form': lote_form,

        })
# def insight_AI(request):
#     return render(request, 'home/dashboard/index.html',{
#         'service': lambda: gerar_insights()
#     })