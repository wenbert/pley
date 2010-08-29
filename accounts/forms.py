from django import forms
from registration.forms import RegistrationFormUniqueEmail

class CustomRegistrationForm(RegistrationFormUniqueEmail):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address1 = forms.CharField(max_length=250, required=False)
    address2 = forms.CharField(max_length=250, required=False)
    city = forms.CharField(max_length=250, required=False)
    province = forms.CharField(max_length=250, required=False)
    zipcode = forms.CharField(max_length=10, required=False)

