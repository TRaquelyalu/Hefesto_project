from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import re

# Validador de CPF
def validar_cpf(value):
    cpf = re.sub(r'\D', '', value)
    if len(cpf) != 11 or not cpf.isdigit():
        raise ValidationError('CPF inválido. Deve conter 11 dígitos.')

# Modelo de Usuário personalizado
class Usuario(AbstractUser):
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    email = models.EmailField(unique=True, verbose_name="E-mail")

    REQUIRED_FIELDS = ['email', 'nome']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

# Perfil do Usuário
class Profile(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='profile')
    cpf = models.CharField(max_length=14, unique=True, validators=[validar_cpf], blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    nome_completo = models.CharField(max_length=150, blank=True, null=True)
    objetivo = models.TextField(blank=True, null=True)
    formacao = models.TextField(blank=True, null=True)
    experiencia = models.TextField(blank=True, null=True)
    habilidades = models.TextField(blank=True, null=True)
    idiomas = models.TextField(blank=True, null=True)
    certificacoes = models.TextField(blank=True, null=True)
    links = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

# Modelo de Vaga
class Vaga(models.Model):
    TIPO_VAGA_CHOICES = [
        ('CLT', 'CLT'),
        ('Freelance', 'Freelance'),
        ('Estágio', 'Estágio'),
    ]
    STATUS_CHOICES = [
        ('Aberta', 'Aberta'),
        ('Fechada', 'Fechada'),
        ('Pendente', 'Pendente'),
    ]
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    localizacao = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    tipo_de_vaga = models.CharField(max_length=20, choices=TIPO_VAGA_CHOICES, default='CLT')
    beneficios = models.TextField(blank=True, null=True)
    carga_horaria = models.CharField(max_length=50, blank=True, null=True)
    prazo_inscricao = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Aberta')

    def __str__(self):
        return self.titulo

# Modelo de Inscrição
class Inscricao(models.Model):
    usuario = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='inscricoes')
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name='inscricoes')
    data_inscricao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'vaga')

    def __str__(self):
        return f"{self.usuario.user.username} -> {self.vaga.titulo}"










