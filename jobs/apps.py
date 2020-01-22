# jobs/apps.py
from django.apps import AppConfig
from django.conf import settings


class JobsConfig(AppConfig):
    name = 'jobs'

    # Autostart the job scheduler
    def ready(self):
        if settings.SCHEDULER_AUTOSTART:
        	try:
                from jobs.scheduler import scheduler
                scheduler.start()
                print("Job scheduler started.")
            except Exception as e:
                print(e)

            