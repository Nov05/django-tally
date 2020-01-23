# yelp/urls.py

from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
# view functions
from .views import home
from .views import hello


urlpatterns = {
    path('<slug:business_id>', home, name='home'),
    path('', hello, name='hello'),
}

urlpatterns = format_suffix_patterns(urlpatterns)