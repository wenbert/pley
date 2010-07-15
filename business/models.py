from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime 

# Create your models here.
BUSINESS_STATUS = (
    ('A', 'Active'),
    ('P', 'Pending'),
    ('I', 'Inactive'),
)

YES_NO_NOTSURE = (
    ('yes', 'Yes'),
    ('no', 'No'),
    ('not_sure', 'Not Sure'),
)

STATUSES = (
    ('on','On'),
    ('off','Off'),
)

ALCOHOL = (
    ('beer','Beer Only'),
    ('wine','Wine Only'),
    ('beer_wine','Beer and Wine'),
    ('full_bar','Full Bar'),
    ('none','None'),
    ('not_sure','Not Sure'),
)

ATTIRE = (
    ('casual','Casual'),
    ('dressy','Dressy'),
    ('formal','Formal (Jacket Required)'),
    ('not_sure','Not Sure'),
)

def validate_max_rating(val):
    if not val in range(1,6):
        raise ValidationError(u'%s is not a valid rating.' % val)


class Business(models.Model):
    name            = models.CharField(max_length=250)
    price_range     = models.IntegerField(validators=[validate_max_rating], verbose_name="Price Range", help_text="1 = Lowest; 5 = Highest")
    credit_card     = models.CharField(max_length=10, verbose_name="Accepts Credit Card?", choices=YES_NO_NOTSURE)
    alcohol         = models.CharField(max_length=25, verbose_name="Serves alcohol?", choices=ALCOHOL)
    kids            = models.CharField(max_length=10, verbose_name="Good for kids?", choices=YES_NO_NOTSURE)
    groups          = models.CharField(max_length=10, verbose_name="Good for groups?", choices=YES_NO_NOTSURE)
    reservations    = models.CharField(max_length=10, verbose_name="Takes reservations?", choices=YES_NO_NOTSURE)
    takeout         = models.CharField(max_length=10, verbose_name="Take-out?", choices=YES_NO_NOTSURE)
    waiters         = models.CharField(max_length=10, verbose_name="Waiter services?", choices=YES_NO_NOTSURE)
    outdoor_seating = models.CharField(max_length=10, verbose_name="Outdoor seating?", choices=YES_NO_NOTSURE)
    wheelchair      = models.CharField(max_length=10, verbose_name="Wheelchair accessible?", choices=YES_NO_NOTSURE)
    attire          = models.CharField(max_length=50, choices=ATTIRE)
    status          = models.CharField(max_length=1, choices=BUSINESS_STATUS, default='A')
    created_at      = models.DateTimeField(verbose_name='Date Created', default=datetime.now, blank=True)
    updated_at      = models.DateTimeField(verbose_name='Date Updated', default=datetime.now, blank=True)
    def __unicode__(self):
        return self.name

class Parking(models.Model):
    business            = models.OneToOneField(Business)
    parking_open        = models.BooleanField(verbose_name='Open Parking')
    parking_basement    = models.BooleanField(verbose_name='Basement Parking')
    parking_private_lot = models.BooleanField(verbose_name='Private Lot')
    parking_valet       = models.BooleanField(verbose_name='Valet Parking')
    parking_validated   = models.BooleanField(verbose_name='Validated')
    parking_street      = models.BooleanField(verbose_name='Street Parking')

class ServingTime(models.Model):
    business        = models.OneToOneField(Business)
    breakfast       = models.BooleanField(verbose_name="Breakfast")
    brunch          = models.BooleanField(verbose_name="Brunch")
    lunch           = models.BooleanField(verbose_name="Lunch")
    inner           = models.BooleanField(verbose_name="Dinner")
    late_night      = models.BooleanField(verbose_name="Late Night")
    dessert         = models.BooleanField(verbose_name="Dessert")
    
class Address(models.Model):
    business        = models.ForeignKey(Business)
    address1        = models.CharField(max_length=250, verbose_name="Address 1")
    address2        = models.CharField(max_length=250, verbose_name="Address 2")
    city            = models.CharField(max_length=250, verbose_name="City")
    province        = models.CharField(max_length=250, verbose_name="Province / State")
    country         = models.CharField(max_length=250, verbose_name="Country")
    zipcode         = models.CharField(max_length=10, verbose_name="Zipcode")
    
class Zipcode(models.Model):
    zipcode         = models.CharField(max_length=10, verbose_name="Zipcode")
    province        = models.CharField(max_length=250, verbose_name="Province")
    city            = models.CharField(max_length=250, verbose_name="City")
    country         = models.CharField(max_length=250, verbose_name="Country")
    def __unicode__(self):
        return self.zipcode