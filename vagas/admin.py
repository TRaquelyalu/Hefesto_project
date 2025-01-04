from django.contrib import admin
from .models import Vaga, Profile

# Registro do modelo Vaga no admin
@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'empresa', 'localizacao', 'tipo_de_vaga', 'data_publicacao')
    search_fields = ('titulo', 'empresa', 'localizacao', 'tipo_de_vaga')
    list_filter = ('tipo_de_vaga', 'localizacao', 'data_publicacao')

# Registro do modelo Profile no admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo_usuario')
    search_fields = ('user__username', 'tipo_usuario')
    list_filter = ('tipo_usuario',)

