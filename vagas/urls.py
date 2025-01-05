from django.urls import path
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from . import views

urlpatterns = [
    # Página inicial dinâmica
    path('', views.index, name='index'),

    # Vagas
    path('vagas/listar/', views.listar_vagas, name='listar_vagas'),
    path('vagas/criar/', views.criar_vaga, name='criar_vaga'),
    path('vagas/editar/<int:id>/', views.editar_vaga, name='editar_vaga'),
    path('vagas/excluir/<int:id>/', views.excluir_vaga, name='excluir_vaga'),

    # Inscrições
    path('vagas/inscrever/<int:vaga_id>/', views.inscrever, name='inscrever'),
    path('vagas/candidatar-se/<int:vaga_id>/', views.candidatar_se, name='candidatar_se'),
    path('vagas/inscricoes/', views.listar_inscricoes, name='listar_inscricoes'),
    path('vagas/excluir-inscricao/<int:id>/', views.excluir_inscricao, name='excluir_inscricao'),

    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='vagas/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),

    # Gerenciamento de perfil (apenas candidatos)
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/', views.ver_perfil, name='ver_perfil'),

    # Páginas adicionais
    path('sobre-nos/', views.sobre_nos, name='sobre_nos'),
    path('contato/', views.contato, name='contato'),
    path('termos-de-uso/', views.termos_de_uso, name='termos_de_uso'),

    # Teste ou desenvolvimento (opcional)
    path('test/', lambda request: render(request, 'vagas/test.html'), name='test'),
]




















