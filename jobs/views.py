# jobs/views.py
import json
from json2html import *
from django.http import HttpResponse
from django.shortcuts import render
# Local imports
from tallylib.logs import getViewLogs
from tallylib.sql import getLogs
# jobs/views.py

# Create your views here.

# Query strings
def home(request, business_id):
    try:
    # get certain number of job logs for a business_id 
    # e.g. http://127.0.0.1:8000/jobs/logs/jga_2HO_j4I7tSYf5cCEnQ
        num = request.GET.get('num')
        result = json2html.convert(json.dumps(getViewLogs(business_id, num)))
        return HttpResponse(result)
    except:
        return None

# nothing here, just say hello
def hello(request):
    result = "Hello, you are at the Jobs application home page."
    return HttpResponse(result)
