from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    # Página inicial
    path('', views.index, name='index'),

    # Vagas
    path('vagas/', views.listar_vagas, name='listar_vagas'),
    path('vagas/criar/', views.criar_vaga, name='criar_vaga'),
    path('vagas/editar/<int:id>/', views.editar_vaga, name='editar_vaga'),
    path('vagas/excluir/<int:id>/', views.excluir_vaga, name='excluir_vaga'),
    path('vagas/<int:id>/', views.detalhes_vaga, name='detalhes_vaga'),

    # Inscrições
    path('vagas/inscrever/<int:vaga_id>/', views.inscrever, name='inscrever'),
    path('vagas/inscricoes/', views.listar_inscricoes, name='listar_inscricoes'),
    path('vagas/inscricao/excluir/<int:id>/', views.excluir_inscricao, name='excluir_inscricao'),

    # Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    

    # Cadastro separado
    path('cadastro/candidato/', views.cadastro_candidato, name='cadastro_candidato'),
    path('cadastro/empresa/', views.cadastro_empresa, name='cadastro_empresa'),

    # Painéis
    path('painel/candidato/', views.painel_candidato, name='painel_candidato'),
    path('painel/empresa/', views.painel_empresa, name='painel_empresa'),

    # Páginas adicionais
    path('sobre-nos/', views.sobre_nos, name='sobre_nos'),
    path('contato/', views.contato, name='contato'),
    path('termos-de-uso/', views.termos_de_uso, name='termos_de_uso'),

    # Página para visitantes
    path('visitantes/', views.index_visitantes, name='index_visitantes'),

    # Teste ou desenvolvimento
    path('test/', lambda request: render(request, 'vagas/test.html'), name='test'),
]











































