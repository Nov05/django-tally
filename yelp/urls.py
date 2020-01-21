# yelp/urls.py

from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
# view functions
from .views import home
from .views import hello
from .views import YelpReviewCreateView # data maintenance
from .views import YelpReviewDetailsView # data maintenance


urlpatterns = {
    path('<slug:business_id>', home, name='home'),
    path('', hello, name='hello'),
    # example
    # create/get/put/delete yelp scraping data via APIs
    # URL - /yelp/yelpscraping/ (create)
    # URL - /yelp/yelpscraping/9759c0c0-b28a-44ff-b770-4cf303367a60/
    url(r'^yelpscraping/$', YelpReviewCreateView.as_view(), name="create"),
    url(r'^yelpscraping/(?P<pk>[0-9a-f-]+)/$',
        YelpReviewDetailsView.as_view(), name="details"),
}

urlpatterns = format_suffix_patterns(urlpatterns)