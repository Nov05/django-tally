# jobs/urls.py
from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
# view functions
from jobs.views import home
from jobs.views import hello
from jobs.examples import example_hello_world # job examples


urlpatterns = {
    # e.g. http://127.0.0.1:8000/jobs/logs/jga_2HO_j4I7tSYf5cCEnQ
    path('logs/<slug:business_id>', home, name='home'),
    path('', hello, name='hello'),
    path('example', example_hello_world, name='examples')
}

urlpatterns = format_suffix_patterns(urlpatterns)
