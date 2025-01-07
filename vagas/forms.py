from django import forms
from django.contrib.auth.models import User
from .models import Vaga, Inscricao, Profile

# Formulário para Inscrições
class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['nome', 'email', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seu nome'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seu email'
            }),
            'mensagem': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control',
                'placeholder': 'Mensagem para a empresa'
            }),
        }

# Formulário para Perfis de Usuário
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'tipo_usuario',
            'idiomas',
            'formacao_academica',
            'habilidades',
            'experiencia_profissional',
        ]
        widgets = {
            'tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
            'idiomas': forms.Textarea(attrs={
                'rows': 3, 'class': 'form-control', 'placeholder': 'Informe os idiomas que você fala'
            }),
            'formacao_academica': forms.Textarea(attrs={
                'rows': 4, 'class': 'form-control', 'placeholder': 'Informe sua formação acadêmica'
            }),
            'habilidades': forms.Textarea(attrs={
                'rows': 3, 'class': 'form-control', 'placeholder': 'Liste suas habilidades'
            }),
            'experiencia_profissional': forms.Textarea(attrs={
                'rows': 5, 'class': 'form-control', 'placeholder': 'Detalhe sua experiência profissional'
            }),
        }

# Formulário de Cadastro de Empresas
class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'cnpj',
            'inscricao_estadual',
            'razao_social',
            'nome_fantasia',
            'telefone',
            'email_cobranca',
            'endereco',
            'cidade',
            'estado',
            'cep',
        ]
        widgets = {
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'XX.XXX.XXX/XXXX-XX',
            }),
            'inscricao_estadual': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Caso Isento Escreva',
            }),
            'razao_social': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Razão Social',
            }),
            'nome_fantasia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome Fantasia',
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código de área e telefone',
            }),
            'email_cobranca': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@example.com',
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço completo',
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade',
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Estado',
            }),
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CEP',
            }),
        }

# Formulário para Candidatos
class CandidatoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['cpf']
        widgets = {
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Informe seu CPF (Formato: XXX.XXX.XXX-XX)',
            }),
        }

# Formulário de Cadastro Personalizado
class CustomUserCreationForm(forms.ModelForm):
    tipo_usuario = forms.ChoiceField(
        choices=Profile.USER_TYPE_CHOICES,
        required=True,
        label="Você é",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Senha"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Seu nome de usuário'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'Seu email'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                tipo_usuario=self.cleaned_data['tipo_usuario'],
            )
        return user

# Formulário para Vagas
class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = [
            'titulo',
            'descricao',
            'empresa',
            'localizacao',
            'faixa_salarial_minima',
            'faixa_salarial_maxima',
            'tipo_de_vaga',
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Título da vaga'
            }),
            'descricao': forms.Textarea(attrs={
                'rows': 4, 'class': 'form-control', 'placeholder': 'Descrição detalhada da vaga'
            }),
            'empresa': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nome da empresa'
            }),
            'localizacao': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Localização da vaga'
            }),
            'faixa_salarial_minima': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Salário mínimo'
            }),
            'faixa_salarial_maxima': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Salário máximo'
            }),
            'tipo_de_vaga': forms.Select(attrs={'class': 'form-control'}),
        }

