# tasks/urls.py
from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
# view functions
from .views import viewGetYelpBusinesses
from .views import viewGetYelpReviews
from .views import viewGetVizdata


urlpatterns = {
    path('getyelpbusinesses', viewGetYelpBusinesses, name="Get Yelp Businesses"),
    path('getyelpreviews', viewGetYelpReviews, name="Get Yelp Reviews"),
    path('getvizdata', viewGetVizdata, name="Get Visualization Data"),
}

urlpatterns = format_suffix_patterns(urlpatterns)