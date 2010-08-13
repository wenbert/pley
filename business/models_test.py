from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime 

# Create your models here.

BUSINESS_STATUS = (
    ('A', 'Active'),
    ('P', 'Pending'),
    ('I', 'Inactive'),
)

ALCOHOL = (
    ('beer','Beer Only'),
    ('wine','Wine Only'),
    ('beer_wine','Beer and Wine'),
    ('full_bar','Full Bar'),
    ('none','None'),
    ('not_sure','Not Sure'),
)

YES_NO_NOTSURE = (
    ('yes', 'Yes'),
    ('no', 'No'),
    ('not_sure', 'Not Sure'),
)

YES_NO_NOTSURE_FIELD_NAMES = (
    ('credit_card', 'Credit Card'),
    ('kids', 'Good for kids'),
    ('groups', 'Good for groups'),
    ('reservations', 'Accepts reservations'),
    ('takeout', 'Takeout'),
    ('waiters', 'Waiters'),
    ('outdoor_seating', 'Outdoor Seating'),
    ('wheelchair', 'Wheelchair Accessable'),
)

STATUSES = (
    ('on','On'),
    ('off','Off'),
)

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

class Property(models.Model):
    business = models.ForeignKey(Business)

class YesNoNotSureProperty(Property):
    name        = models.CharField(max_length=250, choices=YES_NO_NOTSURE_FIELD_NAMES)
    value       = models.CharField(max_length=20, choices=YES_NO_NOTSURE)

# properties with special values
class AlcoholProperty(Property):
    name = models.CharField(max_length=250, default='alcohol', verbose='Serves alcohol', editable=False)
    value = models.CharField(max_length=20, choices=ALCOHOL)

class ParkingProperty(Property):
    name = models.CharField(max_length=250, default='parking', verbose='Parking', editable=False)
    parking_open        = models.BooleanField(verbose_name='Open Parking')
    parking_basement    = models.BooleanField(verbose_name='Basement Parking')
    parking_private_lot = models.BooleanField(verbose_name='Private Lot')
    parking_valet       = models.BooleanField(verbose_name='Valet Parking')
    parking_validated   = models.BooleanField(verbose_name='Validated')
    parking_street      = models.BooleanField(verbose_name='Street Parking')

class Phone(models.Model):
    business        = models.OneToOneField(Business)
    phone_number    = models.CharField(max_length=100, verbose_name="Telephone")

class Zipcode(models.Model):
    zipcode         = models.CharField(max_length=10, verbose_name="Zipcode")
    province        = models.CharField(max_length=250, verbose_name="Province")
    city            = models.CharField(max_length=250, verbose_name="City")
    country         = models.CharField(max_length=250, verbose_name="Country")
    def __unicode__(self):
        return self.zipcode

class Category(models.Model):
    slug            = models.SlugField(max_length=250)
    display         = models.CharField(max_length=250)
    status          = models.CharField(max_length=3, choices=STATUSES, default='A')
    members         = models.ManyToManyField(Business, through="BusinessCategory")
    # allowed properties
    def __unicode__(self):
        return self.slug
    
class BusinessCategory(models.Model):
    business        = models.ForeignKey(Business)
    category        = models.ForeignKey(Category)
    
    
