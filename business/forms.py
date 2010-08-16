from django import forms
from django.forms import ModelForm, TextInput

from pley.business.models import *

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ('created_at', 'updated_at', 'status', 
                   'num_reviews', 'rating',)
        widgets = {
            'name': TextInput(attrs={'class': 'required', 'minlength':'2'}),
            'website': TextInput(attrs={'class': 'url', 'minlength':'2'}),
        }

class BusinessCategoryForm(forms.ModelForm):
    class Meta:
        model = BusinessCategory
        exclude = ('business')
        
class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        exclude = ('business')
