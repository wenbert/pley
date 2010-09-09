import datetime
from haystack.indexes import *
from haystack import site
from pley.business.models import Business, Zipcode
from pley.review.models import Review

class BusinessIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr="name")
    created_by = CharField(model_attr="created_by")
    
    def get_queryset(self):
        return Business.objects.filter(created_at__lte=datetime.datetime.now())

class ReviewIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr="title")
    review = CharField(model_attr="review")
    user = CharField(model_attr="user")
    
    def get_queryset(self):
        return Review.objects.filter(created_at__lte=datetime.datetime.now())

site.register(Business, BusinessIndex)
#site.register(Review, ReviewIndex)
