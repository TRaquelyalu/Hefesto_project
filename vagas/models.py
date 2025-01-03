from django.db import models

class Vaga(models.Model):
    titulo = models.CharField(max_length=100)  # Nome da vaga
    descricao = models.TextField()  # Descrição da vaga
    empresa = models.CharField(max_length=100)  # Nome da empresa
    localizacao = models.CharField(max_length=100, default="Não especificado")  # Localização
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Salário (opcional)
    data_publicacao = models.DateTimeField(auto_now_add=True)  # Data de publicação

    def __str__(self):
        return self.titulo


class Inscricao(models.Model):
    vaga = models.ForeignKey('Vaga', on_delete=models.CASCADE, related_name='inscricoes')  # Vaga relacionada
    nome = models.CharField(max_length=100)  # Nome do candidato
    email = models.EmailField()  # Email do candidato
    mensagem = models.TextField()  # Mensagem do candidato

    def __str__(self):
        return f"{self.nome} - {self.vaga.titulo}"

