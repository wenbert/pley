from django.db import models
from django.contrib import admin
from pley.business.models import Business, Parking, Address, ServingTime

class ParkingInline(admin.StackedInline):
    model = Parking
    
class ServingTimeInline(admin.StackedInline):
    model = ServingTime

class AddressInline(admin.StackedInline):
    model = Address
    extra = 1

class BusinessAdmin(admin.ModelAdmin):
    radio_fields = {
                    'credit_card': admin.VERTICAL, 
                    'alcohol': admin.HORIZONTAL,
                    'kids': admin.VERTICAL,
                    'groups': admin.VERTICAL,
                    'reservations': admin.VERTICAL,
                    'takeout': admin.VERTICAL,
                    'waiters': admin.VERTICAL,
                    'outdoor_seating': admin.VERTICAL,
                    'wheelchair': admin.VERTICAL,
                    'attire': admin.HORIZONTAL,
                    }
    
    inlines = [
        AddressInline,
        ParkingInline,
        ServingTimeInline
    ]
    
    '''        
    fieldsets = (
        (None, {
            'fields': ('name', 'price_range', 'credit_card', 'alcohol','status')
        }),
        ('Dates', {
            'fields':('created_at','updated_at')
        }),
    )
    '''
        
admin.site.register(Business, BusinessAdmin)
