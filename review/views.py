# Create your views here.
from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.db import transaction
from django.db import IntegrityError, DatabaseError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from pley.business.models import *
from pley.business.forms import PropertiesForm
from pley.review.models import *
from pley.review.forms import *

@login_required
@transaction.commit_manually
def review_add(request, business_id):
    success = False
    error = None

    business = get_object_or_404(Business, id=business_id)
    # TODO: a user can only make one review per business. prompt him to edit his previous review instead

    if request.method == 'POST':
        review_form         = ReviewForm(request.POST)
        property_form       = PropertiesForm(request.POST)
        
        if(review_form.is_valid() and property_form.is_valid() and parking_form.is_valid() and serving_time_form.is_valid()):
            review_text     = review_form.cleaned_data['review']
            rating          = review_form.cleaned_data['rating']

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
            
            parking_open    = property_form.cleaned_data['parking_open']
            parking_basement = property_form.cleaned_data['parking_basement']
            parking_private_lot = property_form.cleaned_data['parking_private_lot']
            parking_valet   = property_form.cleaned_data['parking_valet']
            parking_validated = property_form.cleaned_data['parking_validated']
            parking_street  = property_form.cleaned_data['parking_street']
            
            open_time       = property_form.cleaned_data['open_time']
            close_time       = property_form.cleaned_data['close_time']
            
            try:
                #DO THE SAVES HERE
                review = Review(review=review_text, business=business,
                                user=request.user, rating=rating)
                review.save()
                properties = Properties(review=review,
                                      credit_card=credit_card,
                                      alcohol=alcohol,
                                      kids=kids, groups=groups,
                                      reservations=reservations,
                                      takeout=takeout, waiters=waiters,
                                      outdoor_seating=outdoor_seating,
                                      wheelchair=wheelchair, attire=attire,
                                      parking_open=parking_open,
                                      parking_basement=parking_basement,
                                      parking_private_lot=parking_private_lot,
                                      parking_valet=parking_valet,
                                      parking_validated=parking_validated,
                                      parking_street=parking_street,
                                      open_time=open_time,close_time=close_time)
                properties.save()
                user_properties = UserProperties(properties=properties,
                                                 business=business,
                                                 user=request.user)
                user_properties.save()

                #edit business num_reviews and average rating
                business.num_reviews += 1
                previous_reviews = Review.objects.filter(business=business)
                total_rating = 0
                if previous_reviews:
                    for r in previous_reviews:
                        total_rating += r.rating
                total_rating += rating
                average_rating = total_rating / (len(previous_reviews) + 1)
                business.rating = average_rating
                business.save()

                #edit business.properties
                # get all UserProperties of the business
                user_properties_list = UserProperties.objects.filter(business=business)

            except (IntegrityError), e:
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
        property_form       = PropertiesForm()
    
    data = {
                "review_form": review_form,
                "property_form": property_form,
                "success": success,
                "error": error,
                "business": business,
                "user": request.user,
            }
    return render_to_response("review/review_add.html",
                              data, context_instance=RequestContext(request))
