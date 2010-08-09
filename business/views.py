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
from pley.review.models import *
from pley.business.forms import *
from django.core import serializers
import simplejson as json
import urllib

from geopy import geocoders  
from django.conf import settings

def business_home(request):
    data = {}
    return render_to_response("business/business_home.html",
                          data, context_instance=RequestContext(request))


def business_browse(request):
    #my_objects = get_list_or_404(MyModel, published=True)
    business_list = Business.objects.all().order_by('-created_at')
        
    paginator = Paginator(business_list, settings.PAGE_ITEMS)
    
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    
    try:
        businesses = paginator.page(page)
    except (EmptyPage, InvalidPage):
        businesses = paginator.page(paginator.num_page)

    # get categories
    category_list = []
    for business in businesses.object_list:
        business_category_list = BusinessCategory.objects.filter(business=business)
        categories = []
        for business_category in business_category_list:
            categories.append(business_category.category.display)
        category_list.append(categories)

    business_and_categories_list = zip(businesses.object_list, category_list)
        
    data = {
            "business_list": business_list,
            "businesses": businesses,
            "category_list": category_list,
            "business_and_categories_list": business_and_categories_list,
           }
    return render_to_response("business/business_browse.html",
                              data, context_instance=RequestContext(request))

def business_view_v2(request, business_id):
    business_item   = Business.objects.select_related().get(id=business_id)
    phone_list      = Phone.objects.filter(business=business_item)
    reviews         = Review.objects.filter(business=business_id)
    google_apikey   = settings.GOOGLE_MAPS_KEY
    

    string_location = business_item.name + ' near ' +business_item.address1 + ', ' + business_item.address2 + ', ' + business_item.city + ', ' + business_item.province + ', ' + business_item.country
    urlencoded_string_location = urllib.quote_plus(string_location)
    
    data = {"business_item": business_item,
            "phone_list": phone_list,
            "reviews":reviews,
            "string_location":string_location,
            "view_name": request.path,
            "urlencoded_string_location":urlencoded_string_location,
            "google_apikey":google_apikey,
            }
    return render_to_response("business/business_view_v2.html",
                              data, context_instance=RequestContext(request))


def business_view(request, business_id):
    business_item   = Business.objects.select_related().get(id=business_id)
    phone_list      = Phone.objects.filter(business=business_item)
    reviews         = Review.objects.filter(business=business_id)
    
    #sakto ni? ang GOOGLE_MAP_KEY kay string bya
    #g = geocoders.Google(settings.GOOGLE_MAPS_KEY) 
    #g = geocoders.Google(domain='maps.google.co.uk', resource='maps', output_format='json')
    #g = geocoders.Google(domain='maps.google.com', resource='maps')
    #g = geocoders.Google(domain="google.com", resource='maps/geo')
    
    
    string_location = business_item.name+ ', ' + business_item.address1 + ', '  + business_item.city + ', ' + business_item.province + ', ' + business_item.country
    #string_location = business_item.name + ', ' + business_item.address1 + ', ' + business_item.address2 + ' in ' + business_item.city + ', ' + business_item.province + ', ' + business_item.country
    #string_location = business_item.name
    #string_location = business_item.name + ', ' + business_item.address1 + ', ' + business_item.address2 + ', ' + business_item.province + ', ' + business_item.country
    #string_location = "Jolibee, SM City Cebu"
    
    #geodata = []
    #for place, (lat, lng) in g.geocode(string_location,exactly_one=False):
    #    geodata.append((place, (lat, lng)))

    #geo = geodata
    #geodata_count = len(geodata)
    #initial_lat = geodata[0][1][0] #to be used to initially zoom
    #initial_lng = geodata[0][1][1]
    
    #geodata = json.dumps(geodata)
    urlencoded_string_location = urllib.quote_plus(string_location)
    
    data = {"business_item": business_item,
            "phone_list": phone_list,
            "reviews":reviews,
            "string_location":string_location,
            "view_name": request.path,
            "urlencoded_string_location":urlencoded_string_location,
            }
    return render_to_response("business/business_view.html",
                              data, context_instance=RequestContext(request))

@login_required
@transaction.commit_manually
def business_add(request):
    success = False
    error = None
    if request.method == 'POST':
        business_form       = BusinessForm(request.POST)
        business_category_form = BusinessCategoryForm(request.POST)
        phone_form          = PhoneForm(request.POST)
        
        if (business_form.is_valid() and business_category_form.is_valid() and phone_form.is_valid()):
            
            business_name   = business_form.cleaned_data['name']
            category        = business_category_form.cleaned_data['category']
            address_1       = business_form.cleaned_data['address1']
            address_2       = business_form.cleaned_data['address2']
            address_city    = business_form.cleaned_data['city']
            address_province = business_form.cleaned_data['province']
            address_country = business_form.cleaned_data['country']
            # TODO: zipcode should be found in zipcode table
            address_zipcode = business_form.cleaned_data['zipcode']
            
            phone_number    = phone_form.cleaned_data['phone_number']

            # TODO: catch possible exceptions here
            try:
                business = Business(name=business_name,address1=address_1, address2=address_2,
                                  city=address_city, province=address_province,
                                  country=address_country,
                                  zipcode=address_zipcode)
                business.save()
                
                phone   = Phone(phone_number=phone_number, business=business)
                phone.save()
                
                business_category = BusinessCategory(business=business,category=category)
                business_category.save()
                
            except IntegrityError, e:
                transaction.rollback()
                success = False
                error = e
            else:
                transaction.commit()
                success = True
            #redirect to success page
    else:
        business_form   = BusinessForm()
        business_category_form = BusinessCategoryForm()
        phone_form      = PhoneForm()
        
    data = {
              "business_form": business_form,
              "business_category_form": business_category_form,
              "phone_form": phone_form,
              "success": success,
              "error": error
           }
    return render_to_response("business/business_add.html",
                              data, context_instance=RequestContext(request))

