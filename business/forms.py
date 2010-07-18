from django import forms

from pley.business.models import *

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ('created_at', 'updated_at', 'status', )
        '''
        widgets = {
            'price_range': forms.RadioSelect,
            'credit_card': forms.RadioSelect,
            'alcohol': forms.RadioSelect,
            'kids': forms.RadioSelect,
            'reservations': forms.RadioSelect,
            'groups': forms.RadioSelect,
            'waiters': forms.RadioSelect,
            'outdoor_seating': forms.RadioSelect,
            'wheelchair': forms.RadioSelect,
            'attire': forms.RadioSelect,
            'takeout': forms.RadioSelect,
        }
        '''

class ParkingForm(forms.ModelForm):
    class Meta:
        model = Parking
        exclude = ('business',)

class ServingTimeForm(forms.ModelForm):
    class Meta:
        model = ServingTime
        exclude = ('business',)

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('business',)

class BusinessCategoryForm(forms.ModelForm):
    class Meta:
        model = BusinessCategory
        