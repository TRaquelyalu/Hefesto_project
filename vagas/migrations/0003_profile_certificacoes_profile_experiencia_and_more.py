# Generated by Django 5.1.3 on 2025-01-10 12:27

import vagas.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vagas', '0002_remove_profile_tipo_usuario_alter_profile_cpf_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='certificacoes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='experiencia',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='formacao',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='habilidades',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='idiomas',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='links',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='nome_completo',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='objetivo',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='cpf',
            field=models.CharField(blank=True, max_length=14, null=True, unique=True, validators=[vagas.models.validar_cpf]),
        ),
    ]
