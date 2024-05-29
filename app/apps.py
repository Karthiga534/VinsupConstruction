# from django.apps import AppConfig


# class AppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'app'

from django.apps import AppConfig
from django.db.models.signals import post_save

class YourAppNameConfig(AppConfig):
    name = 'app'

    def ready(self):
        from . import signals  # Import signals module here
