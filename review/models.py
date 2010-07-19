from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime 

class Review(models.Model):
    name            = models.CharField(max_length=250)
    status          = models.CharField(max_length=1, choices=BUSINESS_STATUS, default='A')
    created_at      = models.DateTimeField(verbose_name='Date Created', default=datetime.now, blank=True)
    updated_at      = models.DateTimeField(verbose_name='Date Updated', default=datetime.now, blank=True)
    def __unicode__(self):
        return self.name