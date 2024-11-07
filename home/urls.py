from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index, name='home'),
    # path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
]
