from django.db import models
from django.contrib import admin
from pley.business.models import Business, BusinessParking, Parking

class BusinessParkingInline(admin.TabularInline):
    model = BusinessParking

class BusinessAdmin(admin.ModelAdmin):
        inlines = [
            BusinessParkingInline,
        ]
        
admin.site.register(Business, BusinessAdmin)
admin.site.register(Parking)