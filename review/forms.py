from django import forms

from pley.review.models import *

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('created_at', 'updated_at', 'status', )

class ParkingForm(forms.ModelForm):
    class Meta:
        model = Parking
        exclude = ('business',)

class ServingTimeForm(forms.ModelForm):
    class Meta:
        model = ServingTime
        exclude = ('business',)
