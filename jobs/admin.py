from django.contrib import admin

# Register your models here.
# Django will create maintenance page in Admin.  
from .models import JobConfig

admin.site.register(JobConfig)
