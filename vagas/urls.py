from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('criar/', views.criar_vaga, name='criar_vaga'),
    path('editar/<int:id>/', views.editar_vaga, name='editar_vaga'),
    path('excluir_vaga/<int:id>/', views.excluir_vaga, name='excluir_vaga'),
    path('listar/', views.listar_vagas, name='listar_vagas'),
    path('inscrever/<int:vaga_id>/', views.inscrever, name='inscrever'),
    path('inscrever/<int:vaga_id>/', views.inscrever, name='inscrever')
]
