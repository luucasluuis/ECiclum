from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index, name='home'),
    path('saida/', views.saida, name='saida'),
    path('leitura/', views.ler_qrcode, name='qr_code'),
    # path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('tables/', views.lista_produtos, name='lista_produtos'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('charts/', views.charts, name='charts'),
    path('cards/', views.cards, name='cards'),
]