# jobs/urls.py
from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
# view functions
from jobs.views import hello
from jobs.views import logs
# from jobs.views import reset
from jobs.scheduler import scheduleJobs
from jobs.examples import example_hello_world # job examples

# http://127.0.0.1:8000/jobs/...
urlpatterns = {
    path('', hello, name='hello'),
    # update background jobs
    path('reset', scheduleJobs, name='reset'),
    # check job logs for certain business_id
    # e.g. http://127.0.0.1:8000/jobs/logs/jga_2HO_j4I7tSYf5cCEnQ
    path('logs/<slug:business_id>', logs, name='home'),
    path('example', example_hello_world, name='examples')
}

urlpatterns = format_suffix_patterns(urlpatterns)
