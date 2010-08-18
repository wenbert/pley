from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from pley.business.models import Business
from registration.models import *

from datetime import datetime 

REVIEW_STATUS = (
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

ATTIRE = (
    ('casual','Casual'),
    ('dressy','Dressy'),
    ('formal','Formal (Jacket Required)'),
    ('not_sure','Not Sure'),
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

def validate_max_rating(val):
    if not val in range(0,6):
        raise ValidationError(u'%s is not a valid rating.' % val)

class Review(models.Model):
    review          = models.TextField()
    business        = models.ForeignKey(Business)
    user            = models.ForeignKey(User)
    rating          = models.IntegerField(validators=[validate_max_rating])
    status          = models.CharField(max_length=1, choices=REVIEW_STATUS, default='A')
    created_at      = models.DateTimeField(verbose_name='Date Created', default=datetime.now, blank=True)
    updated_at      = models.DateTimeField(verbose_name='Date Updated', default=datetime.now, blank=True)
    def __unicode__(self):
        return self.review
        
'''
class Property(models.Model):
    business        = models.ForeignKey(Business)
    review          = models.OneToOneField(Review)
    credit_card     = models.CharField(max_length=10, verbose_name="Accepts Credit Card?", choices=YES_NO_NOTSURE, default='not_sure')
    alcohol         = models.CharField(max_length=25, verbose_name="Serves alcohol?", choices=ALCOHOL, default='not_sure')
    kids            = models.CharField(max_length=10, verbose_name="Good for kids?", choices=YES_NO_NOTSURE, default='not_sure')
    groups          = models.CharField(max_length=10, verbose_name="Good for groups?", choices=YES_NO_NOTSURE, default='not_sure')
    reservations    = models.CharField(max_length=10, verbose_name="Takes reservations?", choices=YES_NO_NOTSURE, default='not_sure')
    takeout         = models.CharField(max_length=10, verbose_name="Take-out?", choices=YES_NO_NOTSURE, default='not_sure')
    waiters         = models.CharField(max_length=10, verbose_name="Waiter services?", choices=YES_NO_NOTSURE, default='not_sure')
    outdoor_seating = models.CharField(max_length=10, verbose_name="Outdoor seating?", choices=YES_NO_NOTSURE, default='not_sure')
    wheelchair      = models.CharField(max_length=10, verbose_name="Wheelchair accessible?", choices=YES_NO_NOTSURE, default='not_sure')
    attire          = models.CharField(max_length=50, choices=ATTIRE, default='not_sure')

class Parking(models.Model):
    business            = models.ForeignKey(Business)
    review              = models.OneToOneField(Review)
    parking_open        = models.BooleanField(verbose_name='Open Parking')
    parking_basement    = models.BooleanField(verbose_name='Basement Parking')
    parking_private_lot = models.BooleanField(verbose_name='Private Lot')
    parking_valet       = models.BooleanField(verbose_name='Valet Parking')
    parking_validated   = models.BooleanField(verbose_name='Validated')
    parking_street      = models.BooleanField(verbose_name='Street Parking')

class ServingTime(models.Model):
    business        = models.ForeignKey(Business)
    review          = models.OneToOneField(Review)
    breakfast       = models.BooleanField(verbose_name="Breakfast")
    brunch          = models.BooleanField(verbose_name="Brunch")
    lunch           = models.BooleanField(verbose_name="Lunch")
    dinner           = models.BooleanField(verbose_name="Dinner")
    late_night      = models.BooleanField(verbose_name="Late Night")
    dessert         = models.BooleanField(verbose_name="Dessert")
'''

