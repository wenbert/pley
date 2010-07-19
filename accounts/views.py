from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.forms import UserCreationForm


def create(request):
    create_user_form = UserCreationForm()
    
    data = {'create_user_form' : create_user_form}
    
    return render_to_response("accounts/create.html",
                              data, context_instance=RequestContext(request))
