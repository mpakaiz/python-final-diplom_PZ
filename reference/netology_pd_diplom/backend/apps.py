from django.apps import AppConfig


class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reference.netology_pd_diplom.backend'

    def ready(self):
        """
        импортируем сигналы
        """
