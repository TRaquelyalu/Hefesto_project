# Generated by Django 5.1.3 on 2025-01-04 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vagas', '0006_profile_formacao_profile_idiomas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='experiencia',
            new_name='experiencia_profissional',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='formacao',
            new_name='formacao_academica',
        ),
    ]
