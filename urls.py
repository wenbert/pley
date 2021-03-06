from django.conf.urls.defaults import *
from django.conf import settings
from pley.business.models import Business
from pley.review.models import Review
from pley.business.views import *
from pley.review.views import *
from pley.pley_profiles.forms import ProfileForm
from pley.categories.views import *

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
    (r'^business/view/(?P<business_id>\d+)/$', business_view_v3_localsearch),
    (r'^business/save_latlng/(?P<business_id>\d+)/$', save_latlng),
    (r'^category/filter/$', category_filter),
    (r'^review/add/(?P<business_id>\d+)/$', review_add),
    (r'^review/edit/(?P<business_id>\d+)/$', review_edit),
    (r'^review/read/(?P<review_id>\d+)/$', review_read),
    (r'^accounts/', include('accounts.urls')),
    (r'^profiles/edit', 'profiles.views.edit_profile', {'form_class': ProfileForm,}),
    (r'^profiles/', include('profiles.urls')),
    (r'^search/', include('haystack.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.IMAGES_DOC_ROOT, 'show_indexes': True}),
        (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JS_DOC_ROOT, 'show_indexes': True}),
        (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.CSS_DOC_ROOT, 'show_indexes': True}),
    )
