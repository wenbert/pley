from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object
from django.views.generic import list_detail

from pley.business.models import Business, Parking
from pley.business.views import *
from pley.accounts.views import *

from django.views.generic.simple import direct_to_template
from registration.views import register, activate
from registration.forms import *

from django.contrib.auth.views import login, logout

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

    (r'^$', business_home),
    (r'^admin/', include(admin.site.urls)),
    (r'^business/add/$', business_add),
    (r'^business/browse/$', business_browse),
    (r'^business/view/(?P<business_id>\d+)/$', business_view),
    #Enable this instead of backends.default.urls
    
    #Disabled below since there is no email yet
    #(r'^accounts/', include('registration.backends.default.urls')),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    #url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    #(r'^accounts/register/$', register),
    #(r'^business/browse/$', list_detail.object_list, business_info),
    #(r'^business/browse/page(?P<page>[0-9]+/$)',list_detail.object_list, business_info),
    #url(r'^accounts/login/$',  login),
    #url(r'^accounts/logout/$', logout),
    
    #url(r'^accounts/register/$',
    #   register,
    #   {'backend': 'registration.backends.simple.SimpleBackend', 'form_class': RegistrationFormTermsOfService, 'success_url': '/business/browse', },
    #   name='registration_register'),
          
    #url(r'^accounts/register/closed/$',
    #   direct_to_template,
    #   {'template': 'registration/registration_closed.html'},
    #   name='registration_disallowed'),
    #url(r'^accounts/activate/complete/$',
    #   direct_to_template,
    #   {'template': 'registration/activation_complete.html'},
    #   name='registration_activation_complete'),
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
    # that way it can return a sensible "invalid key" message instead of a
    # confusing 404.
    url(r'^accounts/register/$',
       register,
       {'backend': 'registration.backends.default.DefaultBackend', 'form_class': RegistrationFormUniqueEmail },
       name='registration_register'),
    url(r'^accounts/register/complete/$',
       direct_to_template,
       {'template': 'registration/registration_complete.html'},
       name='registration_complete'),
    url(r'^accounts/register/closed/$',
       direct_to_template,
       {'template': 'registration/registration_closed.html'},
       name='registration_disallowed'),
    (r'^accounts/', include('registration.backends.default.urls')),
    #(r'', include('registration.auth_urls')),
    
)