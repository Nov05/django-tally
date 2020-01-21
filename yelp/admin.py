from django.contrib import admin

# Register your models here.
from .models import TallyuserBusiness
from .models import YelpReview

# Django will enable maintenance of 
# those data models on the admin page.
admin.site.register(TallyuserBusiness)
admin.site.register(YelpReview)