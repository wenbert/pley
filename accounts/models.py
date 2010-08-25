from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    reputation = models.IntegerField()
    address1        = models.CharField(max_length=250, verbose_name="Address 1")
    address2        = models.CharField(max_length=250, verbose_name="Address 2", blank=True, null=True)
    city            = models.CharField(max_length=250, verbose_name="City")
    province        = models.CharField(max_length=250, verbose_name="Province / State")
    country         = models.CharField(max_length=250, verbose_name="Country", default="Philippines")
    zipcode         = models.CharField(max_length=10, verbose_name="Zipcode")

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), {'username': self.user.username})
    get_absolute_url = models.permalink(get_absolute_url)
# Create your models here.
