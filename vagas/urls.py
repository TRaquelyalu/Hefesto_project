from django.urls import path
from . import views

urlpatterns = [
    # Página inicial
    path('', views.index, name='index'),  # Página inicial com todas as vagas

    # Vagas
    path('vagas/', views.listar_vagas, name='listar_vagas'),  # Página de listagem de vagas
    path('vagas/<int:vaga_id>/detalhes/', views.detalhes_vaga, name='detalhes_vaga'),  # Detalhes de uma vaga
    path('vagas/<int:vaga_id>/candidatar/', views.candidatar_vaga, name='candidatar_vaga'),  # Candidatar-se a uma vaga
    path('vagas/criar/', views.criar_vaga, name='criar_vaga'),  # Criar nova vaga
    path('vagas/<int:vaga_id>/candidatos/', views.listar_candidatos_por_vaga, name='listar_candidatos_por_vaga'),  # Listar candidatos por vaga

    # Perfil do usuário
    path('perfil/criar/', views.criar_perfil, name='criar_perfil'),  # Criar perfil
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),  # Editar perfil
    path('perfil/', views.meu_perfil, name='meu_perfil'),  # Visualizar perfil do usuário
    path('perfil/minhas-candidaturas/', views.minhas_candidaturas, name='minhas_candidaturas'),  # Listar candidaturas do usuário

    # Autenticação
    path('register/', views.register, name='register'),  # Registro de usuários
    path('login/', views.login_view, name='login'),  # Login
    path('logout/', views.custom_logout, name='logout'),  # Logout

    # Páginas estáticas
    path('sobre-nos/', views.sobre_nos, name='sobre_nos'),  # Página sobre nós
    path('contato/', views.contato, name='contato'),  # Página de contato
    path('termos-de-uso/', views.termos_de_uso, name='termos_de_uso'),  # Página de termos de uso
]




















































