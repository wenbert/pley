from django import forms

from pley.review.models import *
from django.forms.widgets import *

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('created_at', 'updated_at', 'status', 'business', 'user',)

