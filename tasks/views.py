# tasks/views.py
from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
## Local imports
from tallylib.yelpapis import getBusinessesViaAPI


# Create your views here.

def getYelpBusinesses(request):
    try:
        location = request.GET.get('location') # e.g. NYC
        categories = request.GET.get('categories') # e.g. cafe,coffee
        getBusinessesViaAPI(location=location, categories=categories)
        return HttpResponse("yes!")
    except Exception as e:
        print(e)
        return HttpResponse(e)

