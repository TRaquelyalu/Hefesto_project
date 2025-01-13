from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Vaga, Candidatura, Profile


# Formulário de Cadastro de Usuário Personalizado
class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu e-mail'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme sua senha'}),
        }

    def clean_email(self):
        """
        Valida se o e-mail já está registrado.
        """
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email


# Formulário para Candidaturas
class CandidaturaForm(forms.ModelForm):
    class Meta:
        model = Candidatura
        fields = ['vaga']
        widgets = {
            'vaga': forms.HiddenInput(),
        }

    def clean_vaga(self):
        """
        Valida se a vaga está disponível e evita duplicidade de candidatura.
        """
        vaga = self.cleaned_data.get('vaga')
        candidato = self.initial.get('candidato')  # Pegamos o candidato do contexto inicial
        if Candidatura.objects.filter(vaga=vaga, candidato=candidato).exists():
            raise forms.ValidationError("Você já se candidatou a esta vaga.")
        return vaga


# Formulário para Perfis
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['cpf', 'telefone', 'objetivo', 'formacao', 'experiencia', 'habilidades', 'idiomas', 'certificacoes', 'links']
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu CPF'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu telefone'}),
            'objetivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descreva seu objetivo profissional'}),
            'formacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ex.: Curso, Instituição, Ano de Conclusão'}),
            'experiencia': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Descreva sua experiência profissional'}),
            'habilidades': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ex.: Python, Django, SQL'}),
            'idiomas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ex.: Inglês fluente, Espanhol básico'}),
            'certificacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ex.: Curso de Python, Certificação em Django'}),
            'links': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ex.: LinkedIn, GitHub'}),
        }

# Formulário para Vagas
class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['titulo', 'descricao', 'localizacao', 'salario', 'tipo', 'beneficios', 'status', 'prazo_inscricao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o título da vaga'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Descreva a vaga'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a localização'}),
            'salario': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o salário'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o tipo da vaga'}),
            'beneficios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descreva os benefícios'}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o status da vaga'}),
            'prazo_inscricao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


