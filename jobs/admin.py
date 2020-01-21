# jobs/admin.py
from django.contrib import admin
## Local imports 
from .models import JobConfig
from .models import JobLog


# Register your models here.
# Django will create maintenance page in Admin. 
admin.site.register(JobConfig)

## Job logs can be displayed via URL rather than the admin page.
## e.g. http://127.0.0.1:8000/jobs/logs/jga_2HO_j4I7tSYf5cCEnQ
admin.site.register(JobLog)