from django import forms
from .models import Vaga, Inscricao, Profile

# Formulário para Perfis de Usuário
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['foto', 'bio', 'habilidades', 'experiencia_profissional', 'formacao_academica', 'idiomas', 'tipo_usuario']
        widgets = {
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Escreva uma breve biografia'}),
            'habilidades': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Liste suas habilidades'}),
            'experiencia_profissional': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Detalhe sua experiência profissional'}),
            'formacao_academica': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Informe sua formação acadêmica'}),
            'idiomas': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Informe os idiomas que você fala'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
        }

# Formulário para Vagas
class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título da vaga'}),
            'descricao': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Descrição detalhada da vaga'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da empresa'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Localização da vaga'}),
            'faixa_salarial_minima': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salário mínimo'}),
            'faixa_salarial_maxima': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salário máximo'}),
            'tipo_de_vaga': forms.Select(attrs={'class': 'form-control'}),
        }

# Formulário para Inscrições
class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['nome', 'email', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu email'}),
            'mensagem': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Mensagem para a empresa'}),
        }
