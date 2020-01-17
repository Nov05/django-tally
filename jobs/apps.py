# jobs/apps.py
from django.apps import AppConfig
from django.conf import settings

class JobsConfig(AppConfig):
    name = 'jobs'

    def ready(self):
        from . import scheduler
        if settings.SCHEDULER_AUTOSTART:
        	scheduler.start()