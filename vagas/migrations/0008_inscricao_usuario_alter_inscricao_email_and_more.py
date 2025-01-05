# Generated by Django 5.1.3 on 2025-01-04 22:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vagas', '0007_rename_experiencia_profile_experiencia_profissional_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='inscricao',
            name='usuario',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Usuário associado'),
        ),
        migrations.AlterField(
            model_name='inscricao',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='E-mail do candidato'),
        ),
        migrations.AlterField(
            model_name='inscricao',
            name='mensagem',
            field=models.TextField(verbose_name='Mensagem do candidato'),
        ),
        migrations.AlterField(
            model_name='inscricao',
            name='nome',
            field=models.CharField(max_length=100, verbose_name='Nome do candidato'),
        ),
        migrations.AlterField(
            model_name='inscricao',
            name='vaga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscricoes', to='vagas.vaga', verbose_name='Vaga relacionada'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='Biografia'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='experiencia_profissional',
            field=models.TextField(blank=True, null=True, verbose_name='Experiência profissional'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='formacao_academica',
            field=models.TextField(blank=True, null=True, verbose_name='Formação acadêmica'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/', verbose_name='Foto de perfil'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='habilidades',
            field=models.TextField(blank=True, null=True, verbose_name='Habilidades'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='idiomas',
            field=models.TextField(blank=True, null=True, verbose_name='Idiomas'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='tipo_usuario',
            field=models.CharField(choices=[('Candidato', 'Candidato'), ('Recrutador', 'Recrutador')], default='Candidato', max_length=20, verbose_name='Tipo de usuário'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.AlterField(
            model_name='vaga',
            name='data_publicacao',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data de publicação'),
        ),
        migrations.AlterField(
            model_name='vaga',
            name='descricao',
            field=models.TextField(verbose_name='Descrição da vaga'),
        ),
        migrations.AlterField(
            model_name='vaga',
            name='empresa',
            field=models.CharField(max_length=100, verbose_name='Empresa contratante'),
        ),
        migrations.AlterField(
            model_name='vaga',
            name='faixa_salarial_maxima',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Salário máximo'),
        ),
        migrations.AlterField(
            model_name='vaga',
            name='faixa_salarial_minima',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Salário mínimo'),
        ),
        migrations.AlterField(
            model_name='vaga',
            name='localizacao',
            field=models.CharField(default='Não especificado', max_length=100, verbose_name='Localização'),
        ),
        migrations.AlterField(
            model_name='vaga',
            name='tipo_de_vaga',
            field=models.CharField(choices=[('CLT', 'CLT'), ('PJ', 'Pessoa Jurídica'), ('Estágio', 'Estágio'), ('Temporário', 'Temporário')], default='CLT', max_length=50, verbose_name='Tipo de vaga'),
        ),
        migrations.AlterField(
            model_name='vaga',
            name='titulo',
            field=models.CharField(max_length=100, verbose_name='Título da vaga'),
        ),
    ]
