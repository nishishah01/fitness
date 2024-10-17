# apps.py
from django.apps import AppConfig

class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        import main.signals  # Ensure this imports your signals.py
