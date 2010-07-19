#hello
from django.db import models
from django.contrib import admin
from pley.business.models import *

class AddressInline(admin.StackedInline):
    model = Address
    extra = 1

class BusinessCategoryInline(admin.StackedInline):
    model = BusinessCategory
    extra = 1
    
class PhoneInline(admin.StackedInline):
    model = Phone
    extra = 1

class BusinessAdmin(admin.ModelAdmin):
    radio_fields = {}
    
    inlines = [
        AddressInline,
        BusinessCategoryInline,
        PhoneInline,
    ]
        
admin.site.register(Business, BusinessAdmin)
admin.site.register(Category)
