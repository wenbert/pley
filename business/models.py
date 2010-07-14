from django.db import models
from django.core.exceptions import ValidationError

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
    status          = models.CharField(max_length=1, choices=BUSINESS_STATUS)
    created_at      = models.DateTimeField('date created')
    updated_at      = models.DateTimeField('date updated')
    def __unicode__(self):
        return self.name

class Parking(models.Model):
    slug            = models.SlugField(max_length=50)
    display         = models.CharField(max_length=50)
    status          = models.CharField(max_length=5, choices=STATUSES)
    def __unicode__(self):
        return self.display
        
class BusinessParking(models.Model):
    business        = models.ForeignKey(Business)
    parking         = models.ForeignKey(Parking)

