from pathlib import Path
import os
from django.contrib.messages import constants as messages

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta - importante configurar em variáveis de ambiente em produção
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-rv%j5qagxnxh0s)8*8el%x04ng3q7cj3+h^sm^eps*+_-ulat3')

# Modo de depuração - alterar para False em produção
DEBUG = True

# Hosts permitidos - configurar o domínio ou IP em produção
ALLOWED_HOSTS = ['127.0.0.1']


# Aplicativos instalados
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vagas',  # Aplicativo principal do projeto
    'crispy_forms',          # Django Crispy Forms
    'crispy_bootstrap5',     # Estilo Bootstrap 5
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Modelo de usuário personalizado
AUTH_USER_MODEL = 'vagas.Usuario'

# URLs principais
ROOT_URLCONF = 'hefesto_project.urls'

# Configuração de templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'vagas' / 'templates'],  # Caminho para os templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuração do WSGI
WSGI_APPLICATION = 'hefesto_project.wsgi.application'

# Configuração do banco de dados - usar PostgreSQL em produção
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validação de senhas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Arquivos estáticos e de mídia
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Diretório de arquivos estáticos
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Diretório de coleta para produção

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuração de mensagens do Django
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Configurações de autenticação
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Configurações de segurança em produção
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"








