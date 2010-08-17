from django.db import models
from django.contrib import admin
from pley.business.models import *
from pley.review.models import *
class ReviewAdmin(admin.ModelAdmin):
    radio_fields = {}
    
admin.site.register(Review, ReviewAdmin)
