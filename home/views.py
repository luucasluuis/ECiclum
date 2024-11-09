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


def custom_404(request, exception):
    return render(request, 'home/dashboard/404.html', status=404)


def lista_produtos(request):
    produtos = Produto.objects.all()

    # # ------------- Filtragem dos produtos ------------ #
    # nome_produto = request.POST.get('nome', '')
    # setor_armazenamento = request.POST.get('setor', '')
    # if nome_produto or setor_armazenamento:
    #     if nome_produto:
    #         produtos = produtos.filter(nome=nome_produto)
        
    #     if setor_armazenamento:
    #         produtos = produtos.filter(setor_armazenamento=setor_armazenamento)
    # else:
    #    produtos = produtos.all()   

    # produtos = produtos.order_by('vencimento')

        # ------------ Paginação dos produtos ------------- #
    paginator = Paginator(produtos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'home/dashboard/tables.html',
        {
            'produtos': produtos,
        }
    )

def dashboard(request):
    return render(
        request,
        'home/dashboard/index.html'
        )

def charts(request):
    return render(
        request,
        'home/dashboard/charts.html'
        )

def cards(request):
    return render(
        request,
        'home/dashboard/cards.html'
        )