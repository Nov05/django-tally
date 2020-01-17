# jobs/admin.py
from django.contrib import admin
## Local imports 
from .models import JobConfig

# Register your models here.
# Django will create maintenance page in Admin. 
admin.site.register(JobConfig)
