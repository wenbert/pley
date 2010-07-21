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
def review_add(request):
    success = False
    error = None
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        
        if(review_form.is_valid()):
            pass
        else:
            pass
    else:
        review_form = ReviewForm()
    
    data = {
                "review_form": review_form,
                "success": success,
                "error": error
            }
    return render_to_response("review/review_add.html",
                              data, context_instance=RequestContext(request))