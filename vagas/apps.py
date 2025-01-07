from django.apps import AppConfig

class VagasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vagas'

    def ready(self):
        try:
            import vagas.signals  # Somente se você usa signals
        except ImportError:
            pass  # Ignora se não houver signals configurados



