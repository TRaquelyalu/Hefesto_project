from django.db import models
from django.contrib.auth.models import User

# Modelo para Vagas
class Vaga(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título da vaga")  # Nome da vaga
    descricao = models.TextField(verbose_name="Descrição da vaga")  # Descrição da vaga
    empresa = models.CharField(max_length=100, verbose_name="Empresa contratante")  # Nome da empresa
    localizacao = models.CharField(max_length=100, default="Não especificado", verbose_name="Localização")  # Localização
    faixa_salarial_minima = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Salário mínimo"
    )  # Salário mínimo
    faixa_salarial_maxima = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Salário máximo"
    )  # Salário máximo
    tipo_de_vaga = models.CharField(
        max_length=50,
        choices=[
            ('CLT', 'CLT'),
            ('PJ', 'Pessoa Jurídica'),
            ('Estágio', 'Estágio'),
            ('Temporário', 'Temporário'),
        ],
        default='CLT',
        verbose_name="Tipo de vaga"
    )  # Tipo da vaga
    data_publicacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de publicação")  # Data de publicação

    def __str__(self):
        return self.titulo


# Modelo para Inscrições
class Inscricao(models.Model):
    vaga = models.ForeignKey(
        Vaga, on_delete=models.CASCADE, related_name='inscricoes', verbose_name="Vaga relacionada"
    )  # Vaga relacionada
    nome = models.CharField(max_length=100, verbose_name="Nome do candidato")  # Nome do candidato
    email = models.EmailField(verbose_name="E-mail do candidato")  # Email do candidato
    mensagem = models.TextField(verbose_name="Mensagem do candidato")  # Mensagem do candidato
    usuario = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Usuário associado"
    )  # Novo campo para o usuário associado

    def __str__(self):
        return f"{self.nome} - {self.vaga.titulo}"


# Modelo para Perfis de Usuário
class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('Candidato', 'Candidato'),
        ('Recrutador', 'Recrutador'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', verbose_name="Usuário"
    )  # Relacionamento com User
    tipo_usuario = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default='Candidato', verbose_name="Tipo de usuário"
    )  # Tipo de usuário
    foto = models.ImageField(
        upload_to='profile_pics/', null=True, blank=True, verbose_name="Foto de perfil"
    )  # Foto de perfil
    bio = models.TextField(null=True, blank=True, verbose_name="Biografia")  # Biografia
    habilidades = models.TextField(null=True, blank=True, verbose_name="Habilidades")  # Habilidades
    experiencia_profissional = models.TextField(
        blank=True, null=True, verbose_name="Experiência profissional"
    )  # Experiência
    formacao_academica = models.TextField(
        blank=True, null=True, verbose_name="Formação acadêmica"
    )  # Formação acadêmica
    idiomas = models.TextField(null=True, blank=True, verbose_name="Idiomas")  # Idiomas

    def __str__(self):
        return f"{self.user.username} - {self.tipo_usuario}"
