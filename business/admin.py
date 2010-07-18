#hello
from django.db import models
from django.contrib import admin
from pley.business.models import Business, Parking, Address, ServingTime, Category, BusinessCategory, BusinessProperty

class ParkingInline(admin.StackedInline):
    model = Parking
    
class ServingTimeInline(admin.StackedInline):
    model = ServingTime

class AddressInline(admin.StackedInline):
    model = Address
    extra = 1

class BusinessCategoryInline(admin.StackedInline):
    model = BusinessCategory
    extra = 1
    
class BusinessPropertyInline(admin.StackedInline):
    model = BusinessProperty
    extra = 1

class BusinessAdmin(admin.ModelAdmin):
    radio_fields = {}
    
    inlines = [
        AddressInline,
        BusinessCategoryInline,
    ]
        
admin.site.register(Business, BusinessAdmin)
admin.site.register(Category)
