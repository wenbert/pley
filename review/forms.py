from django import forms

from pley.review.models import *
from django.forms.widgets import *

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('created_at', 'updated_at', 'status', 'business', 'user',)

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ('business', 'review',)
        widgets = {
            'credit_card': RadioSelect(),
            'alcohol': RadioSelect(),
            'kids': RadioSelect(),
            'groups': RadioSelect(),
            'reservations': RadioSelect(),
            'takeout': RadioSelect(),
            'waiters': RadioSelect(),
            'outdoor_seating': RadioSelect(),
            'wheelchair': RadioSelect(),
            'attire': RadioSelect(),
        }

class ParkingForm(forms.ModelForm):
    class Meta:
        model = Parking
        exclude = ('business', 'review',)

class ServingTimeForm(forms.ModelForm):
    class Meta:
        model = ServingTime
        exclude = ('business', 'review',)
