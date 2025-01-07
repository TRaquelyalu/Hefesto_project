from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


# Validações de CPF e CNPJ
def validar_cpf(value):
    """Valida o formato de CPF."""
    if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', value):
        raise ValidationError('CPF inválido. Use o formato XXX.XXX.XXX-XX.')


def validar_cnpj(value):
    """Valida o formato de CNPJ."""
    if not re.match(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', value):
        raise ValidationError('CNPJ inválido. Use o formato XX.XXX.XXX/XXXX-XX.')


# Modelo para Vagas
class Vaga(models.Model):
    titulo = models.CharField(max_length=100, verbose_name=_("Título da vaga"))
    descricao = models.TextField(verbose_name=_("Descrição da vaga"))
    empresa = models.CharField(max_length=100, verbose_name=_("Empresa contratante"))
    localizacao = models.CharField(max_length=100, default="Não especificado", verbose_name=_("Localização"))
    faixa_salarial_minima = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Salário mínimo")
    )
    faixa_salarial_maxima = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Salário máximo")
    )
    tipo_de_vaga = models.CharField(
        max_length=50,
        choices=[
            ('CLT', 'CLT'),
            ('PJ', 'Pessoa Jurídica'),
            ('Estágio', 'Estágio'),
            ('Temporário', 'Temporário'),
        ],
        default='CLT',
        verbose_name=_("Tipo de vaga")
    )
    data_publicacao = models.DateTimeField(auto_now_add=True, verbose_name=_("Data de publicação"))

    def clean(self):
        """Validação personalizada para faixa salarial."""
        if self.faixa_salarial_minima and self.faixa_salarial_maxima:
            if self.faixa_salarial_minima > self.faixa_salarial_maxima:
                raise ValidationError(_("O salário mínimo não pode ser maior que o salário máximo."))

    class Meta:
        ordering = ['-data_publicacao']
        verbose_name = _("Vaga")
        verbose_name_plural = _("Vagas")

    def __str__(self):
        return self.titulo


# Modelo para Inscrições
class Inscricao(models.Model):
    vaga = models.ForeignKey(
        Vaga, on_delete=models.CASCADE, related_name='inscricoes', verbose_name=_("Vaga relacionada")
    )
    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="inscricoes", verbose_name=_("Usuário"), null=True, blank=True
    )
    nome = models.CharField(max_length=100, verbose_name=_("Nome do candidato"))
    email = models.EmailField(verbose_name=_("E-mail do candidato"))
    mensagem = models.TextField(
        verbose_name=_("Mensagem do candidato"), blank=True, null=True, default="Sem mensagem"
    )

    def clean(self):
        """Validação personalizada para limitar a mensagem."""
        if self.mensagem and len(self.mensagem) > 500:
            raise ValidationError(_("Mensagem não pode exceder 500 caracteres."))

    class Meta:
        ordering = ['vaga', 'nome']
        verbose_name = _("Inscrição")
        verbose_name_plural = _("Inscrições")

    def __str__(self):
        return f"{self.nome} - {self.vaga.titulo}"


# Modelo para Perfis de Usuário
class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('Candidato', 'Candidato'),
        ('Empresa', 'Empresa'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Usuário")
    tipo_usuario = models.CharField(max_length=50, choices=USER_TYPE_CHOICES, default='Candidato', verbose_name="Tipo de usuário")
    cpf = models.CharField(max_length=14, null=True, blank=True, validators=[validar_cpf], verbose_name="CPF")  # Apenas para Candidatos
    cnpj = models.CharField(max_length=18, null=True, blank=True, validators=[validar_cnpj], verbose_name="CNPJ")  # Apenas para Empresas
    inscricao_estadual = models.CharField(max_length=20, null=True, blank=True, verbose_name="Inscrição Estadual")
    razao_social = models.CharField(max_length=255, null=True, blank=True, verbose_name="Razão Social")
    nome_fantasia = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nome Fantasia")
    telefone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefone")
    email_cobranca = models.EmailField(null=True, blank=True, verbose_name="E-mail de Cobrança")
    endereco = models.CharField(max_length=255, null=True, blank=True, verbose_name="Endereço")
    cidade = models.CharField(max_length=100, null=True, blank=True, verbose_name="Cidade")
    estado = models.CharField(max_length=2, null=True, blank=True, verbose_name="Estado")
    cep = models.CharField(max_length=10, null=True, blank=True, verbose_name="CEP")
    foto = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name="Foto de perfil")
    bio = models.TextField(null=True, blank=True, verbose_name="Biografia")
    idiomas = models.TextField(null=True, blank=True, verbose_name="Idiomas")
    formacao_academica = models.TextField(null=True, blank=True, verbose_name="Formação Acadêmica")
    habilidades = models.TextField(null=True, blank=True, verbose_name="Habilidades")
    experiencia_profissional = models.TextField(null=True, blank=True, verbose_name="Experiência Profissional")

    
    class Meta:
        ordering = ['user__username']
        verbose_name = _("Perfil")
        verbose_name_plural = _("Perfis")

    def __str__(self):
        return f"{self.user.username} - {self.tipo_usuario}"












