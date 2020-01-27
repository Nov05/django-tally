# jobs/scheduler.py
import time
import logging
from datetime import datetime
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerAlreadyRunningError
from django_apscheduler.jobstores import register_events
from django_apscheduler.jobstores import register_job
# local imports
from tallylib.sql import getJobConfig
from tasks.tasks import task_yelpScraper
from tasks.tasks import task_getVizdata


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
def scheduleJobs():
    if settings.DEBUG:
        # Hook into the apscheduler logger
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    # get job configurations
    # [(job_id, job_desc, job_rate, timestamp)]
    job_configs = getJobConfig()

    try:
        for job_id, _, job_rate, _ in job_configs:
            if job_id == 'task_yelpScraper' and job_rate > 0:
                scheduler.add_job(
                    task_yelpScraper,
                    'interval',
                    days=job_rate,
                    id='task_yelpScraper',
                    max_instances=1,
                    replace_existing=True,
                    misfire_grace_time=100)
            elif job_id == "task_getVizdata" and job_rate > 0:
                scheduler.add_job(
                    task_getVizdata,
                    'interval',
                    days=job_rate,
                    id="task_getVizdata",
                    max_instances=1, 
                    replace_existing=True,
                    misfire_grace_time=100)

        register_events(scheduler)
        scheduler.start()
    except Exception as e:
        print(e)

    # Print out scheduled job list
    text = ''
    for job in scheduler.get_jobs():
        text = text + str(job) + '\n'
    text = ("""\n\n\
========================================================
Jobs scheduled: \n""" 
+ text + """\
========================================================
\n""")
    print(text)
    return text.replace('\n', '<br>')


scheduleJobs()


###################################################################
# Run Jobs Immediately
###################################################################
def triggerJobs(job_id):
    ## schedule a job that runs immediately
    try:
        if job_id == "task_yelpScraper":
            scheduler.get_job(job_id="task_yelpScraper").modify(next_run_time=datetime.now())
        elif job_id == "task_getVizdata":
            scheduler.get_job(job_id="task_getVizdata").modify(next_run_time=datetime.now())
    except Exception as e:
        print(e)
        return str(e)
    return f"Next run time to run <b>{job_id}</b> is set to now."


###################################################################
# Pause Jobs
###################################################################
def pauseJobs():
    try:
        for job in scheduler.get_jobs():
            job.pause()
    except Exception as e:
        print(e)
        return (str(e))
    return "Jobs are paused."

###################################################################
# Resume Jobs
###################################################################
def resumeJobs():
    try:
        for job in scheduler.get_jobs():
            job.resume()
    except Exception as e:
        print(e)
        return(str(e))
    return "Jobs are resumed."

    