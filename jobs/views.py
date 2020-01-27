# jobs/views.py
# Create your views here
import json
from django.http import HttpResponse
from django.shortcuts import render
# Local imports
from jobs.logs import getViewJobLogs
from jobs.scheduler import scheduleJobs
from jobs.scheduler import triggerJobs
from jobs.scheduler import pauseJobs
from jobs.scheduler import resumeJobs


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


# Job scheduler instructions
def hello(request):
    result = """\
Hello, you are at the Jobs application home page. <br><br>

You can change the job configurations at page <br>
<b><a href="http://127.0.0.1:8000/admin/jobs/jobconfig/">http://127.0.0.1:8000/admin/jobs/jobconfig/</a></b> <br><br>

You can change jobs by request URL http://&lt;host&gt;/jobs/&lt;operation&gt; <br>
... ... schedule jobs, <b><a href="http://127.0.0.1:8000/jobs/schedule">http://127.0.0.1:8000/jobs/schedule</a></b> <br>
... ... trigger jobs immediately, <br>
... ... ... ... <b><a href="http://127.0.0.1:8000/jobs/trigger?job_id=task_getVizdata">
http://127.0.0.1:8000/jobs/trigger?job_id=task_getVizdata</a></b> <br>
... ... ... ... <b><a href="http://127.0.0.1:8000/jobs/trigger?job_id=task_yelpScraper">
http://127.0.0.1:8000/jobs/trigger?job_id=task_yelpScraper</a></b> <br>
... ... pause jobs, <b><a href="http://127.0.0.1:8000/jobs/pause">http://127.0.0.1:8000/jobs/pause</a></b> <br>
... ... resume jobs, <b><a href="http://127.0.0.1:8000/jobs/resume">http://127.0.0.1:8000/jobs/resume</a></b> <br><br>

You can query job logs for a business by request URL </b>http://&lt;host&gt;/jobs/logs/<business_id></b> <br>
... ... e.g. <b><a href="http://127.0.0.1:8000/jobs/logs/jga_2HO_j4I7tSYf5cCEnQ">http://127.0.0.1:8000/jobs/logs/jga_2HO_j4I7tSYf5cCEnQ</a></b>
"""
    return HttpResponse(result)


# Note: It is not safe to open these APIs to the internet...
# 2020-01-25 You can try to custome the admin page, and move the urls there.
#     Right now I don't have time to do this.
def schedule(request):
    result = scheduleJobs()
    return HttpResponse(result)

def trigger(request):
    try:
        job_id = request.GET.get('job_id')
        result = triggerJobs(job_id)
        return HttpResponse(result)
    except Exception as e:
        print(e)
        return HttpResponse(e)

def pause(request):
    result = pauseJobs()
    return HttpResponse(result)

def resume(request):
    result = resumeJobs()
    return HttpResponse(result)