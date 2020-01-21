from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from rest_framework import generics
import requests
import json
# Local imports
from tallylib.textrank import yelpTrendyPhrases
from tallylib.scattertxt import getDataViztype0
from tallylib.statistics import yelpReviewCountMonthly
from .models import YelpReview                # for data maintenance
from .serializers import YelpReviewSerializer # for data maintenance


# Query strings -> Main analytics
def home(request, business_id):
    viztype = request.GET.get('viztype')
    if viztype == '1':
        result = json.dumps(yelpTrendyPhrases(business_id), 
                            sort_keys=False)
    elif viztype == '2':
        result = json.dumps(yelpReviewCountMonthly(business_id), 
                            sort_keys=False)
    else: # viztype0 and viztype3
        result = json.dumps(getDataViztype0(business_id),
                            sort_keys=False)
    return HttpResponse(result)


# Nothing here
def hello(request):
    result = "Hello, you are at the Tally Yelp Analytics home page."
    return HttpResponse(result)


# example
class YelpReviewCreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = YelpReview.objects.all()
    serializer_class = YelpReviewSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()


# example
class YelpReviewDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = YelpReview.objects.all()
    serializer_class = YelpReviewSerializer

