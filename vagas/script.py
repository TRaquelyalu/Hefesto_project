import os
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hefesto_project.settings')
django.setup()

# Código adicional
from vagas.models import Profile

# Exemplo: listar todos os perfis
perfis = Profile.objects.all()
for perfil in perfis:
    print(perfil)
