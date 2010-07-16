from django import forms

from pley.business.models import *

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ('created_at', 'updated_at', 'status', )

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

