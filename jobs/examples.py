# jobs/examples.py
import os
import time
import logging
from datetime import datetime
from django.conf import settings
from apscheduler.schedulers import SchedulerAlreadyRunningError
from django_apscheduler.jobstores import register_events
from django_apscheduler.jobstores import register_job
from django.http import HttpResponse
# Local imports
from jobs.scheduler import scheduler


'''
This example job "helloworld" will be scheduled by API request
http://127.0.0.1:8000/jobs/example
'''


def helloworld():
    print(r'''
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
    try:
        scheduler.add_job(helloworld,
                          'interval',
                          seconds=5,
                          id=job_id,
                          max_instances=1,
                          replace_existing=True,
                          misfire_grace_time=100)
        # Add the scheduled jobs to the Django admin interface
        register_events(scheduler)
    # APScheduler bug:
    # RuntimeError('cannot schedule new futures after shutdown')
    except Exception as e:
        print(e)
        return HttpResponse(str(e))

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

    try:
        scheduler.start()
    except SchedulerAlreadyRunningError as e:
        print(e)
    except Exception as e:
        print(e)
        return HttpResponse(str(e))

    # give job some time to run
    time.sleep(14)

    # those steps involve database commit
    # give them some time to process
    try:
        scheduler.remove_job(job_id)
    except Exception as e:
        print(e)
        return HttpResponse(str(e))

    # scheduler.shutdown()
    print('''\n\n\
========================================================
Return to http://<host>/jobs/example
========================================================
\n\n''')

    return HttpResponse(f'''\
You started the job scheduler, or it was already running. <br>
... Periodic background job '{job_id}' was scheduled. <br>
... Periodic background job '{job_id}' was removed. <br>
... The job scheduler is still running. <br>
<br>
Check your prompt output history. <br>
If it is deployed on AWS Elastic Beanstalk, check "$ eb logs". <br>
<br>
Note: <br>
Ignore the following Django error message. It is somehow misleading. <br>
... ERROR: django_apscheduler.events: <br>
... ... ... ... ... insert or update on table "django_apscheduler_djangojobexecution" <br>
... ... ... ... ... violates foreign key constraint "django_apscheduler_d_job_id_daf5090a_fk_django_ap". <br>
<br>
Monitor jobs at <a href="http://127.0.0.1:8000/admin/django_apscheduler/djangojob/">http://127.0.0.1:8000/admin/django_apscheduler/djangojob/</a>.
''')
