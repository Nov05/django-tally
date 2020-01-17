# jobs/scheduler.py

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
def start():
    pass