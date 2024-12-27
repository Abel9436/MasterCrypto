from django.apps import AppConfig


class McappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mcapp'
    def ready(self):
        import mcapp.signals

