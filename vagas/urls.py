from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.shortcuts import render  # Adicionando o import do render
urlpatterns = [
    # Página inicial
    path('', views.index, name='index'),

    # Vagas
    path('listar/', views.listar_vagas, name='listar_vagas'),
    path('criar/', views.criar_vaga, name='criar_vaga'),
    path('editar/<int:id>/', views.editar_vaga, name='editar_vaga'),
    path('excluir_vaga/<int:id>/', views.excluir_vaga, name='excluir_vaga'),

    # Inscrições
    path('inscrever/<int:vaga_id>/', views.inscrever, name='inscrever'),
    path('inscricoes/', views.listar_inscricoes, name='inscricoes'),
    path('excluir_inscricao/<int:id>/', views.excluir_inscricao, name='excluir_inscricao'),

    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='vagas/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),

    # Páginas adicionais
    path('sobre-nos/', views.sobre_nos, name='sobre_nos'),
    path('contato/', views.contato, name='contato'),
    path('termos-de-uso/', views.termos_de_uso, name='termos_de_uso'),
    path('test/', lambda request: render(request, 'vagas/test.html'), name='test'),
    
]







