from django.urls import path
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from . import views

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
    path('candidatar-se/<int:vaga_id>/', views.candidatar_se, name='candidatar_se'),
    path('inscricoes/', views.listar_inscricoes, name='inscricoes'),
    path('excluir_inscricao/<int:id>/', views.excluir_inscricao, name='excluir_inscricao'),

    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='vagas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),

    # Páginas adicionais
    path('sobre-nos/', views.sobre_nos, name='sobre_nos'),
    path('contato/', views.contato, name='contato'),
    path('termos-de-uso/', views.termos_de_uso, name='termos_de_uso'),

    # Página de teste
    path('test/', lambda request: render(request, 'vagas/test.html'), name='test'),

    # Gerenciamento de perfil
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/', views.ver_perfil, name='ver_perfil'),
]












