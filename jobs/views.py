# jobs/views.py
# Create your views here
import json
from django.http import HttpResponse
from django.shortcuts import render
# Local imports
from tallylib.logs import getViewLogs
from tallylib.sql import getLogs



# nothing here, just say hello
def hello(request):
    result = "Hello, you are at the Jobs application home page."
    return HttpResponse(result)

# Query strings
def logs(request, business_id):
    try:
        # get certain number of job logs for a business_id
        # e.g. http://127.0.0.1:8000/jobs/logs/jga_2HO_j4I7tSYf5cCEnQ
        num = request.GET.get('num')
        return HttpResponse(getViewLogs(business_id, num))
    except:
        return None


# Query strings
# It is not safe to open this to the internet
def update(request, job_type):
    try:
        # schedule jobs for job_type
        # e.g. http://127.0.0.1:8000/jobs?job_type=0
        job_type = request.GET.get('job_type')
        if job_type == 999:  # schedule all job_types
            pass 
        elif job_type == 0: # yelp scraping
            pass
        return HttpResponse('')
    except:
        return None