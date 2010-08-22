#hello
from django.db import models
from django.contrib import admin
from pley.business.models import *
class BusinessCategoryInline(admin.StackedInline):
    model = BusinessCategory
    extra = 1

'''
class PhoneInline(admin.StackedInline):
    model = Phone
    extra = 1

'''
class CategoryAdmin(admin.ModelAdmin):
    pass

class BusinessAdmin(admin.ModelAdmin):
    radio_fields = {}
    inlines = [BusinessCategoryInline, ]
    
admin.site.register(Business, BusinessAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Zipcode)
#admin.site.register(Category)
