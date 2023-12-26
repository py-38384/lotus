import os
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    if os.environ.get('RUN_MAIN'):
        def ready(self):
            from . import updater
            updater.start()