from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        Método executado quando o app é carregado.
        Usado para importar os signals.
        """
        import core.signals  # noqa
