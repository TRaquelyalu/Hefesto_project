from django.apps import AppConfig

class VagasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vagas'

    def ready(self):
        import vagas.signals  # Garante que os sinais são registrados

