from django import forms

from pley.business.models import *

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ('created_at', 'updated_at', 'status', 
                   'num_reviews', 'rating',)

class BusinessCategoryForm(forms.ModelForm):
    class Meta:
        model = BusinessCategory
        exclude = ('business')
        
class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        exclude = ('business')
