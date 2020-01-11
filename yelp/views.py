# coding: utf-8
from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from rest_framework import generics
import requests
import json
# Local
from .models import YelpYelpScraping
from .serializers import YelpYelpScrapingSerializer
from tallylib.textrank import yelpTrendyPhrases
from tallylib.scattertxt import getDataViztype0
from tallylib.statistics import yelpReviewCountMonthly
 

# Nothing here
def hello(request):
    result = "Hello, you are at the Tally Yelp Analytics home page."
    return HttpResponse(result)


# Query strings -> Main analytics
def home(request, business_id):
    viztype = request.GET.get('viztype')
    if viztype == '1':
        result = json.dumps(yelpTrendyPhrases(business_id))
    elif viztype == '2':
        result = json.dumps(yelpReviewCountMonthly(business_id))
    else:
        result = json.dumps(getDataViztype0(business_id))
    return HttpResponse(result)


class YelpYelpScrapingCreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = YelpYelpScraping.objects.all()
    serializer_class = YelpYelpScrapingSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()


class YelpYelpScrapingDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = YelpYelpScraping.objects.all()
    serializer_class = YelpYelpScrapingSerializer

