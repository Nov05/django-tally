import os
import time
import logging
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.jobstores import register_events
from django_apscheduler.jobstores import register_job
from django.http import HttpResponse


'''
This example job "helloworld" will be scheduled by API request
http://127.0.0.1:8000/jobs/example
'''
# Create scheduler to run in a thread inside the application process
scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)


def helloworld():
    print(\
'''
  _    _      _ _                            _     _ _ 
 | |  | |    | | |                          | |   | | |
 | |__| | ___| | | ___   __      _____  _ __| | __| | |
 |  __  |/ _ \ | |/ _ \  \ \ /\ / / _ \| '__| |/ _` | |
 | |  | |  __/ | | (_) |  \ V  V / (_) | |  | | (_| |_|
 |_|  |_|\___|_|_|\___/    \_/\_/ \___/|_|  |_|\__,_(_)
                                                       
''')
    print(
        'Press Ctrl+{0} to exit.\n'.format('Break' if os.name == 'nt' else 'C'))


def example_hello_world(request):
    if settings.DEBUG:
        # Hook into the apscheduler logger
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    # In database, this value goes to django_apscheduler_djangojob.name.
    job_id = 'helloworld'

    # Adding this job here instead of to crons.
    # This will do the following:
    # - Add a scheduled job to the job store on application initialization
    # - The job will execute a model class method at midnight each day
    # - replace_existing in combination with the unique ID prevents duplicate copies of the job
    scheduler.add_job(helloworld,
                      'interval',
                      seconds=1,
                      id=job_id,
                      max_instances=1,
                      replace_existing=True)

    # Add the scheduled jobs to the Django admin interface
    register_events(scheduler)
    # Print out job list
    print("\n\n")
    print("========================================================")
    print("Jobs scheduled: ")
    # scheduler.print_jobs()
    for j in scheduler.get_jobs():
        print("\t", j)
    print("========================================================")
    print("\n\n")

    try:
        scheduler.start()
        print("scheduler.start()")
    except Exception as e:  # SchedulerAlreadyRunningError
        return HttpResponse(str(e))

    time.sleep(3)
    scheduler.remove_job(job_id)
    scheduler.shutdown()

    return HttpResponse(f'''\
You started the job scheduler. <br>
... Job '{job_id}' was scheduled. <br>
... Job '{job_id}' was removed. <br>
... The job scheduler has been shut down. <br>
<br>
Check your prompt output history. <br>
<br>
Note: <br>
Ignore the following Django error message. It is somehow misleading. <br>
... ERROR: django_apscheduler.events: <br>
... ... ... ... ... insert or update on table "django_apscheduler_djangojobexecution" <br>
... ... ... ... ... violates foreign key constraint "django_apscheduler_d_job_id_daf5090a_fk_django_ap". <br>
''')