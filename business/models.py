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

ALCOHOL = (
    ('beer_wine','Beer and Wine Only'),
    ('full_bar','Full Bar'),
    ('none','None'),
    ('not_sure','Not Sure'),
)
'''
PARKING = (
    ('open_parking','Open Parking'),
    ('basement_parking','Basement Parking'),
    ('street_parking','Street Parking'),
    ('private_lot','Private Lot'),
    ('garage','Garage'),
    ('validated','Validated'),
    ('valet','Valet'),
)'''

STATUSES = (
    ('on','On'),
    ('off','Off'),
)

def validate_max_rating(val):
    if not val in range(1,6):
        raise ValidationError(u'%s is not a valid rating.' % val)


class Business(models.Model):
    name            = models.CharField(max_length=250)
    price_range     = models.IntegerField(validators=[validate_max_rating])
    credit_card     = models.CharField(max_length=10, choices=YES_NO_NOTSURE)
    alcohol         = models.CharField(max_length=25, choices=ALCOHOL)
    status          = models.CharField(max_length=1, choices=BUSINESS_STATUS, default='A')
    created_at      = models.DateTimeField(verbose_name='Date Created', default=datetime.now, blank=True)
    updated_at      = models.DateTimeField(verbose_name='Date Updated', default=datetime.now, blank=True)
    def __unicode__(self):
        return self.name


class Parking(models.Model):
    business        = models.OneToOneField(Business)
    parking_open    = models.BooleanField(verbose_name='Open')
    parking_basement    = models.BooleanField(verbose_name='Basement')
    parking_private_lot    = models.BooleanField(verbose_name='Private Lot')
    parking_valet    = models.BooleanField(verbose_name='Valet')
    parking_validated    = models.BooleanField(verbose_name='Validated')
    parking_street    = models.BooleanField(verbose_name='Street')
