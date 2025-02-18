from django.apps import AppConfig


class BanklotkovConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'banklotkov'

    def ready(self) -> None:
        import banklotkov.signals
