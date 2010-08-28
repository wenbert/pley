from django.db import models
from django.contrib.auth.models import User
from registration import signals

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    reputation = models.IntegerField(default=0)
    address1        = models.CharField(max_length=250, verbose_name="Address 1",blank=True, null=True)
    address2        = models.CharField(max_length=250, verbose_name="Address 2", blank=True, null=True)
    city            = models.CharField(max_length=250, verbose_name="City",blank=True, null=True)
    province        = models.CharField(max_length=250, verbose_name="Province / State",blank=True, null=True)
    country         = models.CharField(max_length=250, verbose_name="Country", default="Philippines",blank=True, null=True)
    zipcode         = models.CharField(max_length=10, verbose_name="Zipcode")

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), {'username': self.user.username})
    get_absolute_url = models.permalink(get_absolute_url)

def create_user_profile(sender, **kwargs):
    '''Create a user profile for the user after registering'''
    user = kwargs['user']
    profile = UserProfile(user=user)
    profile.save()

signals.user_registered.connect(create_user_profile)

