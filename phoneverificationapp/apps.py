from django.apps import AppConfig


class PhoneverificationappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'phoneverificationapp'

    def ready(self):
        import phoneverificationapp.signals