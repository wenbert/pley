from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from datetime import datetime 
# Create your models here.

BUSINESS_STATUS = (
    ('A', 'Active'),
    ('P', 'Pending'),
    ('I', 'Inactive'),
)

STATUSES = (
    ('on','On'),
    ('off','Off'),
)

PROPERTIES = (
    ('credit_card', 'Credit card'),
    ('alcohol', 'Alcohol'),
    ('kids', 'Kids'),
    ('groups', 'Groups'),
    ('reservations', 'Reservations'),
    ('takeout', 'Takeout'),
    ('waiters', 'Waiters'),
    ('outdoor_seating', 'Outdoor seating'),
    ('wheelchair', 'Wheelchair'),
    ('attire', 'Attire'),
)

YES_NO_NOTSURE = (
    ('yes', 'Yes'),
    ('no', 'No'),
    ('not_sure', 'Not Sure'),
    ('not_applicable', 'Not Applicable'),
)

ALCOHOL = (
    ('beer','Beer Only'),
    ('wine','Wine Only'),
    ('beer_wine','Beer and Wine'),
    ('full_bar','Full Bar'),
    ('none','None'),
    ('not_sure','Not Sure'),
    ('not_applicable', 'Not Applicable'),
)

ATTIRE = (
    ('casual','Casual'),
    ('dressy','Dressy'),
    ('formal','Formal (Jacket Required)'),
    ('not_sure','Not Sure'),
    ('not_applicable', 'Not Applicable'),
)

'''
PROP_TYPES = (
    ('checkbox', 'Checkbox'),
    ('textbox', 'Textbox'),
    ('radio', 'Radio'),
    ('select', 'Select'),
    ('multiple', 'Multiple'),
)
'''

def validate_max_rating(val):
    if not val in range(0,6):
        raise ValidationError(u'%s is not a valid rating.' % val)


class Business(models.Model):
    name            = models.CharField(max_length=250)
    website         = models.CharField(max_length=250, blank=True)
    address1        = models.CharField(max_length=250, verbose_name="Address 1")
    address2        = models.CharField(max_length=250, verbose_name="Address 2", blank=True)
    city            = models.CharField(max_length=250, verbose_name="City")
    province        = models.CharField(max_length=250, verbose_name="Province / State")
    country         = models.CharField(max_length=250, verbose_name="Country") #default this to Philippines?
    zipcode         = models.CharField(max_length=10, verbose_name="Zipcode")
    num_reviews     = models.IntegerField(default=0)
    rating          = models.IntegerField(default=0, validators=[validate_max_rating])

    status          = models.CharField(max_length=1, choices=BUSINESS_STATUS, default='A')
    created_at      = models.DateTimeField(verbose_name='Date Created', default=datetime.now, blank=True)
    updated_at      = models.DateTimeField(verbose_name='Date Updated', default=datetime.now, blank=True)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name            = models.CharField(max_length=250)
    slug            = models.CharField(max_length=250)
    status          = models.CharField(max_length=3, choices=STATUSES, default='A')
    members         = models.ManyToManyField(Business, through="BusinessCategory")
    def __unicode__(self):
        return self.slug

class Properties(models.Model):
    credit_card     = models.CharField(max_length=10, verbose_name="Accepts Credit Card?", choices=YES_NO_NOTSURE, default='not_sure')
    alcohol         = models.CharField(max_length=25, verbose_name="Serves alcohol?", choices=ALCOHOL, default='not_sure')
    kids            = models.CharField(max_length=10, verbose_name="Good for kids?", choices=YES_NO_NOTSURE, default='not_sure')
    groups          = models.CharField(max_length=10, verbose_name="Good for groups?", choices=YES_NO_NOTSURE, default='not_sure')
    reservations    = models.CharField(max_length=10, verbose_name="Takes reservations?", choices=YES_NO_NOTSURE, default='not_sure')
    takeout         = models.CharField(max_length=10, verbose_name="Take-out?", choices=YES_NO_NOTSURE, default='not_sure')
    waiters         = models.CharField(max_length=10, verbose_name="Waiter services?", choices=YES_NO_NOTSURE, default='not_sure')
    outdoor_seating = models.CharField(max_length=10, verbose_name="Outdoor seating?", choices=YES_NO_NOTSURE, default='not_sure')
    wheelchair      = models.CharField(max_length=10, verbose_name="Wheelchair accessible?", choices=YES_NO_NOTSURE, default='not_sure')
    attire          = models.CharField(max_length=50, verbose_name="Attire",choices=ATTIRE, default='not_sure')

    parking_open        = models.BooleanField(verbose_name='Open Parking')
    parking_basement    = models.BooleanField(verbose_name='Basement Parking')
    parking_private_lot = models.BooleanField(verbose_name='Private Lot')
    parking_valet       = models.BooleanField(verbose_name='Valet Parking')
    parking_validated   = models.BooleanField(verbose_name='Validated')
    parking_street      = models.BooleanField(verbose_name='Street Parking')

    # TODO: customize time picker widget with http://source.mihelac.org/2010/02/19/django-time-widget-custom-time-shortcuts/
    open_time       = models.TimeField(blank=True)
    close_time      = models.TimeField(blank=True)

class BusinessProperties(models.Model):
    '''
    Normalized properties of a business
    '''
    business        = models.OneToOneField(Business, unique=True)
    properties      = models.OneToOneField(Properties)

class UserProperties(models.Model):
    '''
    User submitted properties.
    To be normalized. 
    '''
    business        = models.ForeignKey(Business)
    user            = models.ForeignKey(User)
    properties      = models.ForeignKey(Properties)

class BusinessCategory(models.Model):
    business        = models.ForeignKey(Business)
    category        = models.ForeignKey(Category)

'''
class BusinessDetailsVal(models.Model):
    business        = models.ForeignKey(Business)


class BusinessDetailsRef(models.Model):
    prop_code       = models.CharField(max_length=250)
    prop_title      = models.CharField(max_length=250)
    prop_type       = models.CharField(max_length=100, choices=PROP_TYPES)
    weight          = models.FloatField()
    status          = models.CharField(max_length=10, choices=STATUSES)

class BusinessDetailsRefValueRef(models.Model):
    business_detail = models.ForeignKey(BusinessDetailsVal)
    value           = models.CharField(max_length=255)
    weight          = models.FloatField()
'''
