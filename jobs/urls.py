# jobs/urls.py
from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
# view functions
from jobs.examples import example_hello_world # job examples
from jobs.views import hello
from jobs.views import logs
from jobs.views import schedule
from jobs.views import trigger
from jobs.views import pause
from jobs.views import resume


# http://<host>/jobs/...
urlpatterns = {
    path('', hello, name='hello'),
    path('schedule', schedule, name='schedule'),
    path('trigger', trigger, name='trigger'),
    path('pause', pause, name='pause'),
    path('resume', resume, name='resume'),
    path('logs/<slug:business_id>', logs, name='home'),
    path('example', example_hello_world, name='examples')
}

urlpatterns = format_suffix_patterns(urlpatterns)