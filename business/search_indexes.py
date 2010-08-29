import datetime
from haystack.indexes import *
from haystack import site
from pley.models import Business

class BusinessIndex(SearchIndex):
    name = CharField(document=True, use_template=True)
    created_at = DateTimeField(model_attr='created_at')
    updated_at = DateTimeField(model_attr='updated_at')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Business.objects.filter(created_at__lte=datetime.datetime.now())


site.register(Business, BusinessIndex)