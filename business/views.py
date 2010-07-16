# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from pley.business.models import *
from pley.business.forms import *

def business_add(request):
    success = False
    if request.method == 'POST':
        business_form = BusinessForm(request.POST)
        address_form = AddressForm(request.POST)
        parking_form = ParkingForm(request.POST)
        serving_time_form = ServingTimeForm(request.POST)

        if (business_form.is_valid() and address_form.is_valid()
        and parking_form.is_valid() and serving_time_form.is_valid()):
            business_name = business_form.cleaned_data['name']
            price_range = business_form.cleaned_data['price_range']
            credit_card = business_form.cleaned_data['credit_card']
            alcohol = business_form.cleaned_data['alcohol']
            kids = business_form.cleaned_data['kids']
            groups = business_form.cleaned_data['groups']
            reservations = business_form.cleaned_data['reservations']
            takeout = business_form.cleaned_data['takeout']
            waiters = business_form.cleaned_data['waiters']
            outdoor_seating = business_form.cleaned_data['outdoor_seating']
            wheelchair = business_form.cleaned_data['wheelchair']
            attire = business_form.cleaned_data['attire']

            parking_open = parking_form.cleaned_data['parking_open']
            parking_basement = parking_form.cleaned_data['parking_basement']
            parking_private_lot = parking_form.cleaned_data['parking_private_lot']
            parking_valet = parking_form.cleaned_data['parking_valet']
            parking_validated = parking_form.cleaned_data['parking_validated']
            parking_street = parking_form.cleaned_data['parking_street']

            address_1 = address_form.cleaned_data['address1']
            address_2 = address_form.cleaned_data['address2']
            address_city = address_form.cleaned_data['city']
            address_province = address_form.cleaned_data['province']
            address_country = address_form.cleaned_data['country']
            # TODO: zipcode should be found in zipcode table
            address_zipcode = address_form.cleaned_data['zipcode']

            serving_breakfast = serving_time_form.cleaned_data['breakfast']
            serving_brunch = serving_time_form.cleaned_data['brunch']
            serving_lunch = serving_time_form.cleaned_data['lunch']
            serving_dinner = serving_time_form.cleaned_data['dinner']
            serving_late_night = serving_time_form.cleaned_data['late_night']
            serving_dessert = serving_time_form.cleaned_data['dessert']

            # TODO: catch possible exceptions here
            business = Business(name=business_name, price_range=price_range,
                                credit_card=credit_card, alcohol=alcohol,
                                kids=kids, groups=groups, takeout=takeout,
                                waiters=waiters, reservations=reservations,
                                outdoor_seating=outdoor_seating,
                                attire=attire,
                                wheelchair=wheelchair)
            business.save()
            parking = Parking(parking_open=parking_open, 
                              parking_basement=parking_basement,
                              parking_private_lot=parking_private_lot,
                              parking_valet=parking_valet,
                              parking_validated=parking_validated,
                              parking_street=parking_street, 
                              business=business)
            address = Address(address1=address_1, address2=address_2,
                              city=address_city, province=address_province,
                              country=address_country,
                              zipcode=address_zipcode,
                              business=business)
            serving_time = ServingTime(breakfast=serving_breakfast,
                                       brunch=serving_brunch,
                                       lunch=serving_lunch,
                                       dinner=serving_dinner,
                                       late_night=serving_late_night,
                                       dessert=serving_dessert, 
                                       business=business)
            parking.save()
            address.save()
            serving_time.save()
            success = True
            #redirect to success page
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
              "success": success
           }
    return render_to_response("business_form.html",
                              data, context_instance=RequestContext(request))

