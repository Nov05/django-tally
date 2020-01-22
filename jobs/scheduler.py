# jobs/scheduler.py
import time
import logging
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerAlreadyRunningError
from django_apscheduler.jobstores import register_events
from django_apscheduler.jobstores import register_job
# local imports
from jobs.tasks import task_yelpScraper


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


###################################################################
# Schedule Jobs for Tasks
###################################################################
if settings.DEBUG:
    # Hook into the apscheduler logger
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)

job_id = "task_yelpScraper"
try:
    scheduler.add_job(task_yelpScraper,
                      'interval',
                      minutes=1,
                      id=job_id,
                      max_instances=1,
                      replace_existing=True,
                      misfire_grace_time=100)
    register_events(scheduler)
    scheduler.start()
except Exception as e:
    print(e)

# Print out scheduled job list
text = ''
for j in scheduler.get_jobs():
    text = text + str(j) + '\n'
print('''\n\n\
========================================================
Jobs scheduled: \n'''
          + text + '''\
========================================================
\n\n''')

# try:
#     scheduler.remove_job(job_id)
# except Exception as e:
#     print(e)