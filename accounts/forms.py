#import profiles

from django import forms
from registration.forms import RegistrationFormUniqueEmail
#from accounts.models import UserProfile

class CustomRegistrationForm(RegistrationFormUniqueEmail):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address1 = forms.CharField(max_length=250, required=False)
    address2 = forms.CharField(max_length=250, required=False)
    city = forms.CharField(max_length=250, required=False)
    province = forms.CharField(max_length=250, required=False)
    zipcode = forms.CharField(max_length=10, required=False)

'''
class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(profiles.ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
        except User.DoesNotExist:
            pass
    email = forms.EmailField(label='Email', help_text='')

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def save(self, *args, **kwargs):
        u = self.instance.user
        u.email = self.cleaned_data['email']
        u.save()
        profile = super(profiles.ProfileForm, self).save(*args, **kwargs)
        return profile
'''

