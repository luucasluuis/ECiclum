# estoque/urls.py
from django.urls import path
from .views import HomeView, SaidaView, LerQRCodeView, DashboardView, ChartsView, CardsView, ProdutoListView, ProdutoCreateView

app_name = 'home'  # Adicione um app_name para usar como namespace

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('saida/', SaidaView.as_view(), name='saida'),
    path('leitura-qrcode/', LerQRCodeView.as_view(), name='ler_qrcode'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('charts/', ChartsView.as_view(), name='charts'),
    path('cards/', CardsView.as_view(), name='cards'),
    path('produtos/', ProdutoListView.as_view(), name='produtos_list'),
    path('produtos/novo/', ProdutoCreateView.as_view(), name='produto_create'),
]
