# Create your views here.
from django.http import HttpResponse
from django.forms.models import inlineformset_factory
from django.template import RequestContext
from django.shortcuts import render_to_response

from pley.business.models import *
from pley.business.forms import *

def business_save(request):
    if request.method == 'POST':
        pass

def business_add(request):
    if request.method == 'POST':
        business_form = BusinessForm(request.POST)
        address_form = AddressForm(request.POST)
        parking_form = ParkingForm(request.POST)
        serving_time_form = ServingTimeForm(request.POST)
        name = business_form.cleaned_data['name']
    else:
        business_form = BusinessForm()
        address_form = AddressForm()
        parking_form = ParkingForm()
        serving_time_form = ServingTimeForm()

    data = {
              "business_form": business_form,
              "address_form": address_form,
              "parking_form": parking_form,
              "serving_time_form": serving_time_form,
              "success": success,
              "name": name,
           }
    return render_to_response("business_form.html",
                              data,
                              context_instance=RequestContext(request, data))
