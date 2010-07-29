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
        property_form       = PropertyForm(request.POST)
        parking_form        = ParkingForm(request.POST)
        serving_time_form   = ServingTimeForm(request.POST)
        
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
                review = Review(review=review_text, business=business,
                                user=request.user, rating=rating)
                review.save()
                properties = Property(business=business,
                                      review=review,
                                      credit_card=credit_card,
                                      alcohol=alcohol,
                                      kids=kids, groups=groups,
                                      reservations=reservations,
                                      takeout=takeout, waiters=waiters,
                                      outdoor_seating=outdoor_seating,
                                      wheelchair=wheelchair, attire=attire)
                parking = Parking(business=business, 
                                  review=review,
                                  parking_open=parking_open,
                                  parking_basement=parking_basement,
                                  parking_private_lot=parking_private_lot,
                                  parking_valet=parking_valet,
                                  parking_validated=parking_validated,
                                  parking_street=parking_street)
                serving_time = ServingTime(business=business,
                                           review=review,
                                           breakfast=breakfast,
                                           brunch=brunch, lunch=lunch,
                                           dinner=dinner, late_night=late_night,
                                           dessert=dessert)
                properties.save()
                parking.save()
                serving_time.save()

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
        property_form       = PropertyForm()
        parking_form        = ParkingForm()
        serving_time_form   = ServingTimeForm()
    
    data = {
                "review_form": review_form,
                "property_form": property_form,
                "parking_form": parking_form,
                "serving_time_form": serving_time_form,
                "success": success,
                "error": error,
                "business": business,
                "user": request.user,
            }
    return render_to_response("review/review_add.html",
                              data, context_instance=RequestContext(request))
