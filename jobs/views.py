# jobs/views.py
# Create your views here
import json
from django.http import HttpResponse
from django.shortcuts import render
# Local imports
from tallylib.sql import getJobLogs
from jobs.logs import getViewJobLogs
from jobs.tasks import task_yelpScraper


# nothing here, just say hello
def hello(request):
    result = "Hello, you are at the Jobs application home page."
    return HttpResponse(result)

# Query strings
def logs(request, business_id):
    result = ''
    try:
        # get certain number of job logs for a business_id
        # e.g. http://127.0.0.1:8000/jobs/logs/jga_2HO_j4I7tSYf5cCEnQ
        num = request.GET.get('num')
        return HttpResponse(getViewJobLogs(business_id, num))
    except:
        return HttpResponse(result)


# Query strings
# It is not safe to open these APIs to the internet.
def schedule(request):
    result = ''
    try:
        # schedule jobs for job_type
        # e.g. http://127.0.0.1:8000/jobs/schedule?job_type=0
        job_type = int(request.GET.get('job_type'))
        if job_type == 999:  # schedule all job_types
            pass 
        elif job_type == 0: # yelp scraping
            task_yelpScraper()
            result = f"You just triggered Yelp scraping."
            return HttpResponse(result)
        else:
            return HttpResponse(result)
    except:
        return HttpResponse(result)