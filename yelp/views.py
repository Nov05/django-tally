from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from rest_framework import generics
import requests
import json
# Local imports
from .models import YelpReview                # example
from .serializers import YelpReviewSerializer # example
from tallylib.textrank import yelpTrendyPhrases
from tallylib.scattertxt import getDataViztype0
from tallylib.statistics import yelpReviewCountMonthly
from tallylib.sql import getLatestVizdata


# Query strings -> Main analytics
# 2020-01-22 Here return codes and messages could be added 
#     to make the APIs more user friendly.
def home(request, business_id):
    '''get data for views (APIs)'''
    result = ""
    try:
        viztype = request.GET.get('viztype')
        data = getLatestVizdata(business_id, viztype=int(viztype)) # a list of tuples
        if len(data) > 0:
                result = data[0][0]
        else:
            if viztype == '0': # viztype0 and viztype3
                result = json.dumps(getDataViztype0(business_id),
                                    sort_keys=False)
            elif viztype == '1':    
                result = json.dumps(yelpTrendyPhrases(business_id), 
                                    sort_keys=False)
            elif viztype == '2':     
                result = json.dumps(yelpReviewCountMonthly(business_id), 
                                sort_keys=False)
            else: 
                result = f"Error: There is no viztype {viztype}."
    except Exception as e:
        print(e)
        result = f"Error: Wrong viztype {viztype}<br>{str(e)}"

    return HttpResponse(result)


# Nothing here
def hello(request):
    result = "Hello, you are at the Tally Yelp Analytics home page."
    return HttpResponse(result)


# example (do NOT change data in tallyds.yelp_review)
class YelpReviewCreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = YelpReview.objects.all()
    serializer_class = YelpReviewSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()


# example (do NOT change data in tallyds.yelp_review)
class YelpReviewDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = YelpReview.objects.all()
    serializer_class = YelpReviewSerializer

