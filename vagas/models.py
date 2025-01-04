from django.db import models
from django.contrib.auth.models import User

# Modelo para Vagas
class Vaga(models.Model):
    titulo = models.CharField(max_length=100)  # Nome da vaga
    descricao = models.TextField()  # Descrição da vaga
    empresa = models.CharField(max_length=100)  # Nome da empresa
    localizacao = models.CharField(max_length=100, default="Não especificado")  # Localização
    faixa_salarial_minima = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Salário mínimo
    faixa_salarial_maxima = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Salário máximo
    tipo_de_vaga = models.CharField(
        max_length=50,
        choices=[
            ('CLT', 'CLT'),
            ('PJ', 'Pessoa Jurídica'),
            ('Estágio', 'Estágio'),
            ('Temporário', 'Temporário'),
        ],
        default='CLT'
    )  # Tipo da vaga
    data_publicacao = models.DateTimeField(auto_now_add=True)  # Data de publicação

    def __str__(self):
        return self.titulo

# Modelo para Inscrições
class Inscricao(models.Model):
    vaga = models.ForeignKey('Vaga', on_delete=models.CASCADE, related_name='inscricoes')  # Vaga relacionada
    nome = models.CharField(max_length=100)  # Nome do candidato
    email = models.EmailField()  # Email do candidato
    mensagem = models.TextField()  # Mensagem do candidato

    def __str__(self):
        return f"{self.nome} - {self.vaga.titulo}"

# Modelo para Perfis de Usuário
class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('Candidato', 'Candidato'),
        ('Recrutador', 'Recrutador'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # Relacionamento com User
    foto = models.ImageField(upload_to='profile_pics/', null=True, blank=True)  # Foto de perfil
    bio = models.TextField(null=True, blank=True)  # Biografia
    habilidades = models.TextField(null=True, blank=True)  # Habilidades
    experiencia = models.TextField(null=True, blank=True)  # Experiência
    tipo_usuario = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='Candidato')  # Tipo de usuário

    def __str__(self):
        return f"{self.user.username} - {self.tipo_usuario}"
