from django.db import models
from django.contrib import admin
from pley.business.models import *
from pley.review.models import *

class ProperyInline(admin.StackedInline):
    model = Property
    extra = 1

class ParkingInline(admin.StackedInline):
    model = Parking
    extra = 1
    
class ServingTimeInline(admin.StackedInline):
    model = ServingTime
    extra = 1

class ReviewAdmin(admin.ModelAdmin):
    radio_fields = {}
    
    inlines = [
        ProperyInline,
        ParkingInline,
        ServingTimeInline,
    ]
        
admin.site.register(Review, ReviewAdmin)
