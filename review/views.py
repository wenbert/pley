# Create your views here.
from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.db import transaction
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from pley.business.models import *
from pley.business.forms import *
from pley.review.models import *
from pley.review.forms import *

@login_required
@transaction.commit_manually
def review_add(request, business_id):
    success = False
    error = None
    if request.method == 'POST':
        review_form         = ReviewForm(request.POST)
        property_form       = PropertyForm(request.POST)
        parking_form        = ParkingForm(request.POST)
        serving_time_form   = ServingTimeForm(request.POST)
        
        if(review_form.is_valid() and property_form.is_valid and parking_form.is_valid and serving_time_form.is_valid):
            review          = review_form.cleaned_data['review']
            
            credit_card     = property_form.cleaned_data['credit_card']
            alcohol         = property_form.cleaned_data['alcohol']
            kids            = property_form.cleaned_data['kids']
            groups          = property_form.cleaned_data['groups']
            reservations    = property_form.cleaned_data['reservations']
            takeout         = property_form.cleaned_data['takeout']
            waiters         = property_form.cleaned_data['waiters']
            outdoor_seating = property_form.cleaned_data['outdoor_seating']
            wheelchair      = property_form.cleaned_data['wheelchair']
            attire          = property_form.cleaned_data['attire']
            
            parking_open    = parking_form.cleaned_data['parking_open']
            parking_basement = parking_form.cleaned_data['parking_basement']
            parking_private_lot = parking_form.cleaned_data['parking_private_lot']
            parking_valet   = parking_form.cleaned_data['parking_valet']
            parking_validated = parking_form.cleaned_data['parking_validated']
            parking_street  = parking_form.cleaned_data['parking_street']
            
            breakfast       = serving_time_form.cleaned_data['breakfast']
            brunch          = serving_time_form.cleaned_data['brunch']
            lunch           = serving_time_form.cleaned_data['lunch']
            dinner          = serving_time_form.cleaned_data['dinner']
            late_night      = serving_time_form.cleaned_data['late_night']
            dessert         = serving_time_form.cleaned_data['dessert']
            
            try:
                #DO THE SAVES HERE
                pass
            except IntegrityError, e:
                transaction.rollback()
                success = False
                error = e
            else:
                transaction.commit()
                success = True
            
        else:
            pass
    else:
        review_form         = ReviewForm()
        property_form       = PropertyForm()
        parking_form        = ParkingForm()
        serving_time_form   = ServingTimeForm()
    
    data = {
                "review_form": review_form,
                "property_form": property_form,
                "parking_form": parking_form,
                "serving_time_form": serving_time_form,
                "success": success,
                "error": error
            }
    return render_to_response("review/review_add.html",
                              data, context_instance=RequestContext(request))