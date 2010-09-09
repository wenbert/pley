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

from datetime import datetime

@login_required
@transaction.commit_manually
def review_add(request, business_id):
    success = False
    error = None

    business = get_object_or_404(Business, id=business_id)
    if request.method == 'POST':
        review_form         = ReviewForm(request.POST)

        if(review_form.is_valid()):
            title           = review_form.cleaned_data['title']
            review_text     = review_form.cleaned_data['review']
            rating          = review_form.cleaned_data['rating']
            excerpt         = ' '.join(review_text.split(' ')[:10]) + '...'
            try:
                #DO THE SAVES HERE
                review = Review(review=review_text, business=business,
                                user=request.user, rating=rating,
                                title=title, excerpt=excerpt)
                print excerpt
                review.save()

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
        review_form = ReviewForm()
    data = {
                "review_form": review_form,
                "success": success,
                "error": error,
                "business": business,
                "user": request.user,
            }
    return render_to_response("review/review_add.html",
                              data, context_instance=RequestContext(request))

@login_required
@transaction.commit_manually
def review_edit(request, business_id):
    success = False
    error = None

    business = get_object_or_404(Business, id=business_id)
    user = request.user
    review = get_object_or_404(Review, business=business, user=user)
    # TODO: a user can only make one review per business. prompt him to edit his previous review instead

    if request.method == 'POST':
        review_form         = ReviewForm(request.POST)

        if(review_form.is_valid()):
            title           = review_form.cleaned_data['title']
            review_text     = review_form.cleaned_data['review']
            rating          = review_form.cleaned_data['rating']

            try:
                #DO THE SAVES HERE
                review.title = title
                review.rating = rating
                review.review = review_text
                review.updated_at = datetime.now()
                review.save()
                #edit business num_reviews and average rating
                previous_reviews = Review.objects.filter(business=business).exclude(user=user)
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
        title = review.title
        review_text = review.review
        rating = review.rating
        initial_data = {
            'title':title,
            'review':review_text,
            'rating':rating,
        }
        review_form = ReviewForm(initial_data)

    data = {
                "review_form": review_form,
                "success": success,
                "error": error,
                "business": business,
                "user": request.user,
            }
    return render_to_response("review/review_add.html",
                              data, context_instance=RequestContext(request))

def review_read(request, business_id):
    error = None
    review = get_object_or_404(Review, business=business_id)
    return render_to_response('review/review_read.html', {'review':review})

