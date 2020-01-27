# tasks/urls.py
from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
# view functions
from .views import getYelpBusinesses


urlpatterns = {
    path('getyelpbusinesses', getYelpBusinesses, name="Get Yelp Businesses"),
}

urlpatterns = format_suffix_patterns(urlpatterns)