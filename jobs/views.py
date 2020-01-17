# jobs/views.py
# Create your views here
import json
from django.http import HttpResponse
from django.shortcuts import render
# Local imports
from tallylib.logs import getViewLogs
from tallylib.sql import getLogs


# Query strings
def home(request, business_id):
    try:
        # get certain number of job logs for a business_id
        # e.g. http://127.0.0.1:8000/jobs/logs/jga_2HO_j4I7tSYf5cCEnQ
        num = request.GET.get('num')
        return HttpResponse(getViewLogs(business_id, num))
    except:
        return None


# nothing here, just say hello
def hello(request):
    result = "Hello, you are at the Jobs application home page."
    return HttpResponse(result)