from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object
from django.views.generic import list_detail

from pley.business.models import Business, Parking
from pley.business.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#to be used in generic views
business_info = {
    "queryset": Business.objects.all(),
    "template_name": "business/business_browse.html",
    "paginate_by": 3,
}

urlpatterns = patterns('',
    # Example:
    # (r'^pley/', include('pley.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    ('^business/add/$', business_add),
    ('^business/browse/$', business_browse),
    #(r'^business/browse/$', list_detail.object_list, business_info),
    #(r'^business/browse/page(?P<page>[0-9]+/$)',list_detail.object_list, business_info),
)
