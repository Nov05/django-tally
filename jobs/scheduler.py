# jobs/scheduler.py
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler


# In jobs/app.py the following code will start the scheduler
# when the "jobs" application starts.
'''
class JobsConfig(AppConfig):
    name = 'jobs'

    def ready(self):
        from . import scheduler
        if settings.SCHEDULER_AUTOSTART:
        	scheduler.start()
'''
# Create scheduler to run in a thread inside the application process
scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)