from django.contrib import admin
from .models import Usuario, Profile, Vaga, Candidatura


# Registro do modelo de Usuário
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name']  # Exibe os campos padrão de AbstractUser
    search_fields = ['username', 'email', 'first_name', 'last_name']  # Busca por nome e sobrenome
    ordering = ['id']  # Ordenação padrão por ID


# Registro do modelo de Perfil
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'cpf', 'telefone', 'data_nascimento']  # Campos relevantes do Profile
    search_fields = ['user__username', 'cpf', 'telefone']  # Busca por username do usuário e CPF
    list_filter = ['data_nascimento']  # Filtro para datas de nascimento
    ordering = ['id']  # Ordenação padrão por ID


# Registro do modelo de Vaga
@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'localizacao', 'salario', 'tipo', 'status', 'data_criacao']  # Adicionados novos campos
    search_fields = ['titulo', 'descricao', 'localizacao']  # Campos de busca
    list_filter = ['localizacao', 'tipo', 'status', 'data_criacao']  # Filtros para facilitar a navegação
    ordering = ['data_criacao']  # Ordenação por data de criação


# Registro do modelo de Candidatura
@admin.register(Candidatura)
class CandidaturaAdmin(admin.ModelAdmin):
    list_display = ['id', 'vaga', 'candidato', 'data_candidatura']  # Exibe as informações principais
    search_fields = ['vaga__titulo', 'candidato__username']  # Busca por título da vaga e username do candidato
    list_filter = ['data_candidatura', 'vaga']  # Filtros úteis
    ordering = ['data_candidatura']  # Ordenação por data de candidatura
    list_select_related = ['vaga', 'candidato']  # Otimização de consultas relacionadas


