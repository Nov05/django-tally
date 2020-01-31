# tasks/views.py
from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
## Local imports
from tallylib.yelpapis import getYelpBusinessesViaAPI
from tallylib.sql import getYelpBusinessIDs
from tallylib.sql import getFailedJobLogs
from tasks.tasks import task_yelpScraper
from tasks.tasks import task_getVizdata


# Create your views here.

def viewGetYelpBusinesses(request):
    try:
        location = request.GET.get('location') # e.g. New York or Phoenix
        categories = request.GET.get('categories') # e.g. cafe,coffee
        mode = request.GET.get('mode') # e.g. testrun 
        result = getYelpBusinessesViaAPI(location=location, categories=categories, mode=mode)
        return HttpResponse(result)
    except Exception as e:
        print(e)
        return HttpResponse(e)


def viewGetYelpReviews(request):
    result = ""
    try:
        location = request.GET.get('location') # e.g. New York or Phoenix
        categories = request.GET.get('categories') # e.g. cafe,coffee
        mode = request.GET.get('mode') # e.g. fix

        business_ids = []
        if mode == 'fix':
            business_ids = getFailedJobLogs()
            print(f"Fixing failed Yelp web scraping tasks for {len(business_ids)} businesses...")
        else:
            business_ids = getYelpBusinessIDs(location=location, categories=categories)
        task_yelpScraper(business_ids)
        result = f"You have web scraped the latest reviews for {len(business_ids)} \
businesses in location '{location}' with categories '{categories}'."
        return HttpResponse(result)
    except Exception as e:
        print(e)
        return HttpResponse(e)


def viewGetVizdata(request):
    result = ""
    try:
        location = request.GET.get('location') # e.g. New York or Phoenix
        categories = request.GET.get('categories') # e.g. cafe,coffee
        business_ids = []
        business_ids = getYelpBusinessIDs(location=location, categories=categories)
        task_getVizdata(business_ids)
        result = f"You have generated visualization data for {len(business_ids)} \
businesses in location '{location}' with categories '{categories}'."
        return HttpResponse(result)
    except Exception as e:
        print(e)
        return HttpResponse(e)
