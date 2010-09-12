from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from datetime import datetime
from pley.categories.models import Category
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

YES_NO_NOTSURE = (
    ('yes', 'Yes'),
    ('no', 'No'),
    ('not_sure', 'Not Sure'),
    ('not_applicable', 'Not Applicable'),
)

DAYS = (
    ('mon','Monday'),
    ('tue','Tuesday'),
    ('wed','Wednesday'),
    ('thu','Thursday'),
    ('fri', 'Friday'),
    ('sat', 'Saturday'),
    ('sun', 'Sunday'),
)


def validate_max_rating(val):
    if not val in range(0,6):
        raise ValidationError(u'%s is not a valid rating.' % val)


class Business(models.Model):
    name            = models.CharField(max_length=250)
    website         = models.CharField(max_length=250, blank=True, null=True)
    address1        = models.CharField(max_length=250, verbose_name="Address 1")
    address2        = models.CharField(max_length=250, verbose_name="Address 2", blank=True, null=True)
    city            = models.CharField(max_length=250, verbose_name="City")
    province        = models.CharField(max_length=250, verbose_name="Province / State")
    country         = models.CharField(max_length=250, verbose_name="Country", default="Philippines")
    zipcode         = models.CharField(max_length=10, verbose_name="Zipcode")
    num_reviews     = models.IntegerField(default=0)
    rating          = models.IntegerField(default=0, validators=[validate_max_rating])
    description     = models.TextField(max_length=500 ,blank=True, null=True)
    lat             = models.FloatField(default=0.0, verbose_name="Latitude")
    lng             = models.FloatField(default=0.0, verbose_name="Longitude")

    status          = models.CharField(max_length=1, choices=BUSINESS_STATUS, default='A')
    created_at      = models.DateTimeField(verbose_name='Date Created', default=datetime.now, blank=True, null=True)
    updated_at      = models.DateTimeField(verbose_name='Date Updated', default=datetime.now, blank=True, null=True)
    created_by      = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/business/view/%i/" % self.id

    class Meta:
        verbose_name = "business"
        verbose_name_plural = "businesses"

#class Category(models.Model):
#    name            = models.CharField(max_length=250, unique=True)
#    slug            = models.CharField(max_length=250, unique=True)
#    status          = models.CharField(max_length=3, choices=STATUSES, default='A')
#    members         = models.ManyToManyField(Business, through="BusinessCategory")
#    def __unicode__(self):
#        return self.slug

class Phone(models.Model):
    business        = models.ForeignKey(Business)
    phone           = models.CharField(max_length=250, verbose_name='Main Phone')
    alternate       = models.CharField(max_length=250, blank=True, null=True, verbose_name='Alternate Phone')
    fax             = models.CharField(max_length=250, blank=True, null=True, verbose_name='Fax')
    mobile          = models.CharField(max_length=250, blank=True, null=True, verbose_name='Mobile Phone')
    def __unicode__(self):
        return self.phone

class Zipcode(models.Model):
    zipcode         = models.CharField(max_length='10')
    major_area      = models.CharField(max_length='50')
    city            = models.CharField(max_length='50')

    def __unicode__(self):
        return '%s : %s : %s' % (self.zipcode, self.major_area, self.city)

    class Meta:
        ordering = ['zipcode']

class BusinessCategory(models.Model):
    business        = models.ForeignKey(Business,db_index=True)
    category        = models.ForeignKey(Category,db_index=True)

    def __unicode__(self):
        return '%s - %s' % (self.business.name, self.category.name)

    class Meta:
        unique_together = (('business', 'category'),)

class BusinessDetails(models.Model):
    business        = models.ForeignKey(Business)
    field_name      = models.CharField(max_length=100, verbose_name="Field Name")
    field_value     = models.CharField(max_length=250, verbose_name="Field Value")

class BusinessHours(models.Model):
    business        = models.ForeignKey(Business)
    day             = models.CharField(max_length=3, verbose_name="Day",choices=DAYS, blank=True)
    time_open_1     = models.TimeField(blank=True, null=True)
    time_open_2     = models.TimeField(blank=True, null=True)
    time_close_1    = models.TimeField(blank=True, null=True)
    time_close_2    = models.TimeField(blank=True, null=True)
    closed          = models.BooleanField()

class BusinessPaymentOptions(models.Model):
    #TODO: change this to OneToOneField
    business        = models.ForeignKey(Business)
    cash            = models.BooleanField(verbose_name="Cash")
    credit_card     = models.BooleanField(verbose_name="Credit Card")
    debit_card      = models.BooleanField(verbose_name="Debit Card")
    cheque          = models.BooleanField(verbose_name="Cheque")
    gift_cert       = models.BooleanField(verbose_name="Gift Certificates")
    others          = models.BooleanField(verbose_name="Others")

