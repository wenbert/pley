import datetime
from haystack.indexes import *
from haystack import site
from pley.business.models import Business, Zipcode

class BusinessIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr='name')

    def get_queryset(self):
        return Business.objects.filter(created_at__lte=datetime.datetime.now())

class ZipcodeIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    zipcode = CharField(model_attr='zipcode')

site.register(Business, BusinessIndex)
site.register(Zipcode, ZipcodeIndex)

