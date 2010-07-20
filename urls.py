from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object
from django.views.generic import list_detail

from pley.business.models import Business, Parking
from pley.business.views import *
from pley.accounts.views import *

from django.views.generic.simple import direct_to_template
from registration.views import register, activate


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#to be used in generic views
#business_info = {
#    "queryset": Business.objects.all(),
#    "template_name": "business/business_browse.html",
#    "paginate_by": 3,
#}

urlpatterns = patterns('',
    # Example:
    # (r'^pley/', include('pley.foo.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^business/add/$', business_add),
    (r'^business/browse/$', business_browse),
    (r'^business/view/(?P<business_id>\d+)/$', business_view),
    #Enable this instead of backends.default.urls
    #(r'^accounts/', include('registration.backends.simple.urls')),
    #Disabled below since there is no email yet
    #(r'^accounts/', include('registration.backends.default.urls')),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    #(r'^accounts/register/$', register),
    #(r'^business/browse/$', list_detail.object_list, business_info),
    #(r'^business/browse/page(?P<page>[0-9]+/$)',list_detail.object_list, business_info),
    url(r'^accounts/register/$',
       register,
       {'backend': 'registration.backends.simple.SimpleBackend', 'success_url': '/business/browse'},
       name='registration_register'),
   url(r'^accounts/register/closed/$',
       direct_to_template,
       {'template': 'registration/registration_closed.html'},
       name='registration_disallowed'),
   (r'', include('registration.auth_urls')),
)