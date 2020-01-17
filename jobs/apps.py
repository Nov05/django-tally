# jobs/apps.py
from django.apps import AppConfig
from django.conf import settings

class JobsConfig(AppConfig):
    name = 'jobs'

    # Autostart the job scheduler
    def ready(self):
        from jobs.scheduler import scheduler
        if settings.SCHEDULER_AUTOSTART:
        	scheduler.start()