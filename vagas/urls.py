from django.urls import path
from . import views

urlpatterns = [
    # Página inicial
    path('', views.index, name='index'),

    # Vagas
    path('vagas/', views.listar_vagas, name='listar_vagas'),
    path('vagas/<int:vaga_id>/detalhes/', views.detalhes_vaga, name='detalhes_vaga'),
    path('vagas/<int:vaga_id>/candidatar/', views.candidatar_vaga, name='candidatar_vaga'),
    path('vagas/criar/', views.criar_vaga, name='criar_vaga'),


    # Perfil
    path('perfil/criar/', views.criar_perfil, name='criar_perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),

    # Autenticação
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),

    # Páginas estáticas
    path('sobre-nos/', views.sobre_nos, name='sobre_nos'),
    path('contato/', views.contato, name='contato'),
    path('termos-de-uso/', views.termos_de_uso, name='termos_de_uso'),
]


















































