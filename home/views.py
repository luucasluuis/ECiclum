from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Produto
from django.core.paginator import Paginator

# @login_required
def index(request):
    return render(
        request,
        'home/home.html')

def saida(request):
    return render(
        request,
        'home/saida.html')

def ler_qrcode(request):
    return render(
        request,
        'home/leitura_qrcode.html')

# def login(request):
#     return render(
#         request,
#         'home/login.html')

def custom_404_view(request):
    return render(
        request,
        '404.html',
        status=404
    )

def lista_produtos(request):
    produtos = Produto.objects

    # ------------ Paginação dos produtos ------------- #
    paginator = Paginator(produtos.all(), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ------------- Filtragem dos produtos ------------ #
    nome_produto = request.POST.get('nome', '')
    setor_armazenamento = request.POST.get('setor', '')
    if nome_produto:
        produtos = produtos.filter(nome=nome_produto)

    if setor_armazenamento:
        produtos = produtos.filter(setor_armazenamento=setor_armazenamento)

    produtos = produtos.order_by('vencimento')

    return render(
        request,
        'home/lista_produtos.html',
        {
            'produtos': produtos,
            'nome_produto': nome_produto,
            'setor_armazenamento': setor_armazenamento,
            'page_obj': page_obj
        }
    )

def analise_de_dados(request):
    pass