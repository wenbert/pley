from django.db import models
from django.contrib import admin
from pley.business.models import Business

class BusinessAdmin(admin.ModelAdmin):
    pass
        
admin.site.register(Business, BusinessAdmin)
