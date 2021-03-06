from django.db import models, transaction, IntegrityError
from django.contrib.auth.models import User
from registration import signals

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    reputation = models.IntegerField(default=0)
    address1        = models.CharField(max_length=250, verbose_name="Address 1",blank=True, null=True)
    address2        = models.CharField(max_length=250, verbose_name="Address 2", blank=True, null=True)
    city            = models.CharField(max_length=250, verbose_name="City",blank=True, null=True)
    province        = models.CharField(max_length=250, verbose_name="Province / State",blank=True, null=True)
    country         = models.CharField(max_length=250, verbose_name="Country", default="Philippines",blank=True, null=True)
    zipcode         = models.CharField(max_length=10, verbose_name="Zipcode",blank=True,null=True)

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), {'username': self.user.username})
    get_absolute_url = models.permalink(get_absolute_url)

@transaction.commit_manually
def create_user_profile(sender, **kwargs):
    '''Create a user profile for the user after registering'''
    print 'creating user profile'
    user = kwargs['user']
    request = kwargs['request']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    address2 = request.POST['address2']
    address1 = request.POST['address1']
    city = request.POST['city']
    province = request.POST['province']
    zipcode = request.POST['zipcode']
    profile = UserProfile(user=user,address1=address1, address2=address2,
                          city=city, province=province,
                          zipcode=zipcode)
    user.first_name = first_name
    user.last_name = last_name

    try:
        profile.save()
    except IntegrityError:
        print "registration.signals.user_registered triggered twice. "
        transaction.rollback()
    else:
        user.save()
        transaction.commit()



#NOTE: this is triggered twice. not sure why.
signals.user_registered.connect(create_user_profile)

