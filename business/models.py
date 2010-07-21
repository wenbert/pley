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

def validate_max_rating(val):
    if not val in range(1,6):
        raise ValidationError(u'%s is not a valid rating.' % val)


class Business(models.Model):
    name            = models.CharField(max_length=250)
    status          = models.CharField(max_length=1, choices=BUSINESS_STATUS, default='A')
    created_at      = models.DateTimeField(verbose_name='Date Created', default=datetime.now, blank=True)
    updated_at      = models.DateTimeField(verbose_name='Date Updated', default=datetime.now, blank=True)
    def __unicode__(self):
        return self.name
        
class Address(models.Model):
    business        = models.ForeignKey(Business)
    address1        = models.CharField(max_length=250, verbose_name="Address 1")
    address2        = models.CharField(max_length=250, verbose_name="Address 2")
    city            = models.CharField(max_length=250, verbose_name="City")
    province        = models.CharField(max_length=250, verbose_name="Province / State")
    # NOTE: kailangan pa country? philippines ra man ka ni?
    country         = models.CharField(max_length=250, verbose_name="Country")
    zipcode         = models.CharField(max_length=10, verbose_name="Zipcode")

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
    def __unicode__(self):
        return self.slug
    
class BusinessCategory(models.Model):
    business        = models.ForeignKey(Business)
    category        = models.ForeignKey(Category)
    
    