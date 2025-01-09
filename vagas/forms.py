from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Vaga, Inscricao, Profile

# Formulário de Cadastro de Usuário Personalizado
class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nome', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

# Formulário para Inscrições
class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['vaga']
        widgets = {
            'vaga': forms.HiddenInput(),
        }

# Formulário para Perfis
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['cpf', 'telefone', 'data_nascimento']
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu CPF'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu telefone'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

# Formulário para Vagas
class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = [
            'titulo', 'descricao', 'localizacao', 'salario',
            'tipo_de_vaga', 'beneficios', 'carga_horaria',
            'prazo_inscricao', 'status'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control'}),
            'salario': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_de_vaga': forms.Select(attrs={'class': 'form-select'}),
            'beneficios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'carga_horaria': forms.TextInput(attrs={'class': 'form-control'}),
            'prazo_inscricao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

