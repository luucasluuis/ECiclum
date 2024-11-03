from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Produto

@login_required
def index(request):

    context = {
        'teste': 'testando'
    }
    return render(
        request,
        'home/home.html',
        context)

def login(request):
    return render(
        request,
        'home/login.html')

def custom_404_view(request, exception):
    return render(
        request,
        '404.html',
        status=404
    )

def lista_produtos(request):
    produtos = Produto.objects
    print(f' ESte é o requeste {request} e tipo {type(request)}')
    nome_produto = request.POST.get('nome', '')
    if nome_produto:
        produtos = produtos.filter(nome='nome_produto').values()
        nome_produto = ""

    setor_armazenamento = request.POST.get('setor', '')
    if setor_armazenamento:
        print('algo')
        setor_armazenamento = ""
        produtos = produtos.filter(setor_armazenamento='setor_armazenamento').values()
        print(setor_armazenamento)

    produtos = produtos.order_by('vencimento')

    return render(
        request,
        'home/lista_produtos.html',
        {
            'produtos': produtos,
            'nome_produto': nome_produto,
            'setor_armazenamento': setor_armazenamento
            }
        )