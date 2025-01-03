from django import forms
from .models import Vaga
from .models import Inscricao

class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = '__all__'  # Ou liste os campos específicos que deseja incluir
class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['nome', 'email', 'mensagem']  # Campos disponíveis no formulário
