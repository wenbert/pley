from django import forms
from django.forms import ModelForm, TextInput

from pley.business.models import *

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ('created_at', 'updated_at', 'status', 
<<<<<<< HEAD
                   'num_reviews', 'rating',)
        widgets = {
            'name': TextInput(attrs={'class': 'required', 'minlength':'2'}),
            'website': TextInput(attrs={'class': 'url', 'minlength':'2'}),
        }
=======
                   'num_reviews', 'rating','properties')

class PropertiesForm(forms.ModelForm):
    class Meta:
        model = Properties
>>>>>>> fa9a8eb126e8bcb668b569b1e3269804f07ebe8f

class BusinessCategoryForm(forms.ModelForm):
    class Meta:
        model = BusinessCategory
        exclude = ('business')
        
class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        exclude = ('business')

