from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
import re


# Validador de CPF
def validar_cpf(value):
    cpf = re.sub(r'\D', '', value)
    if len(cpf) != 11 or not cpf.isdigit():
        raise ValidationError('CPF inválido. Deve conter 11 dígitos.')


# Modelo de Usuário Personalizado
class Usuario(AbstractUser):
    pass


# Perfil do Usuário
class Profile(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='profile')
    cpf = models.CharField(max_length=14, unique=True, validators=[validar_cpf], blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
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
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    localizacao = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    beneficios = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    prazo_inscricao = models.DateField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


# Modelo de Candidatura
class Candidatura(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    candidato = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_candidatura = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidato.username} - {self.vaga.titulo}"


# Sinais para Criar e Salvar Perfis Automáticos
@receiver(post_save, sender=Usuario)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    """
    Cria automaticamente um perfil para cada novo usuário.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Usuario)
def salvar_perfil_usuario(sender, instance, **kwargs):
    """
    Garante que o perfil seja salvo sempre que o usuário for salvo.
    """
    if hasattr(instance, 'profile'):  # Verifica se o perfil existe antes de salvar
        instance.profile.save()

