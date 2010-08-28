from django import forms
from registration.forms import RegistrationFormUniqueEmail

class CustomRegistrationForm(RegistrationFormUniqueEmail):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address1 = forms.CharField(max_length=250)
    address2 = forms.CharField(max_length=250)
    city = forms.CharField(max_length=250)
    province = forms.CharField(max_length=250)
    zipcode = forms.CharField(max_length=10)

