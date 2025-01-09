from django.contrib import admin
from .models import Usuario, Profile, Vaga, Inscricao

# Registro do modelo de Usuário
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'nome']
    search_fields = ['username', 'email', 'nome']

# Registro do modelo de Perfil
if not admin.site.is_registered(Profile):
    @admin.register(Profile)
    class ProfileAdmin(admin.ModelAdmin):
        list_display = ['user', 'cpf', 'telefone', 'data_nascimento']
        search_fields = ['user__username', 'cpf']

# Registro do modelo de Vaga
if not admin.site.is_registered(Vaga):
    @admin.register(Vaga)
    class VagaAdmin(admin.ModelAdmin):
        list_display = ['titulo', 'tipo_de_vaga', 'salario', 'status']
        search_fields = ['titulo', 'descricao', 'localizacao']
        list_filter = ['tipo_de_vaga', 'status']

# Registro do modelo de Inscrição
if not admin.site.is_registered(Inscricao):
    @admin.register(Inscricao)
    class InscricaoAdmin(admin.ModelAdmin):
        list_display = ['usuario', 'vaga', 'data_inscricao']
        search_fields = ['usuario__user__username', 'vaga__titulo']
        list_filter = ['data_inscricao']

