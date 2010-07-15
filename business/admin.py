from django.db import models
from django.contrib import admin
from pley.business.models import Business, Parking

class ParkingInline(admin.StackedInline):
    model = Parking
    extra = 1

class BusinessAdmin(admin.ModelAdmin):
    radio_fields = {'credit_card': admin.VERTICAL, 'alcohol': admin.HORIZONTAL}
    
    inlines = [
        ParkingInline,
    ]
            
    fieldsets = (
        (None, {
            'fields': ('name', 'price_range', 'credit_card', 'alcohol','status')
        }),
        ('Dates', {
            'fields':('created_at','updated_at')
        }),
    )
        
admin.site.register(Business, BusinessAdmin)

'''('Parking', {
            'fields': ('parking_open', 
                       'parking_basement', 
                       'parking_private_lot',
                       'parking_valet',
                       'parking_validated',
                       'parking_street')
        }),'''
