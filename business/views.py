# Create your views here.
from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.db import transaction
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core import serializers
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


def business_view_v3_localsearch(request, business_id):
    business_item   = Business.objects.select_related().get(id=business_id)
    phone_list      = Phone.objects.filter(business=business_item)
    reviews         = Review.objects.filter(business=business_id)
    google_apikey   = settings.GOOGLE_MAPS_KEY
    
    #sakto ni? ang GOOGLE_MAP_KEY kay string bya
    #g = geocoders.Google(settings.GOOGLE_MAPS_KEY) 
    
    #string_location = business_item.name + ' near: ' +business_item.address1 + ', ' + business_item.address2 +  ', ' + business_item.province + ', ' + business_item.country + ', ' + business_item.zipcode
    string_location = business_item.address1 +  ', ' +business_item.address2 +  ', ' + business_item.city +  ', ' + business_item.province + ', ' + business_item.country + ', ' + business_item.zipcode
    clean_string_location = ''.join([letter for letter in string_location if not letter.isdigit()])
    
    urlencoded_string_location = urllib.quote_plus(string_location)
    
    business_form   = BusinessForm()
    business_category_form = BusinessCategoryForm()
    phone_form      = PhoneForm()
    
    data = {"business_item": business_item,
            "phone_list": phone_list,
            "reviews":reviews,
            "string_location":string_location,
            "clean_string_location":clean_string_location,
            "view_name": request.path,
            "urlencoded_string_location":urlencoded_string_location,
            "google_apikey":google_apikey,
            "business_form": business_form,
            "business_category_form": business_category_form,
            "phone_form": phone_form,
            }
    return render_to_response("business/business_view_v3_localsearch.html",
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
            categories.append(business_category.category.name)
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
    
    string_location = ' '+ business_item.name + ' near: ' +business_item.address1 + ', ' + business_item.address2 + ', ' + business_item.city + ', ' + business_item.province + ', ' + business_item.country
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
    
    string_location = ''+business_item.name+ ' near: ' + business_item.address1 + ', ' + business_item.address2 +  ', ' + business_item.province + ', ' + business_item.country
    
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
        business_details_form = BusinessDetailsForm(request.POST)
        business_payment_options_form = BusinessPaymentOptionsForm(request.POST)
        businss_hours_form = BusinessHoursForm(request.POST)

        business_category_form_list = [BusinessCategoryForm(data=request.POST, prefix='business_category_form_'+str(i))
                                       for i in range(5)]

        business_hours_form_list = [BusinessHoursForm(data=request.POST,
                                                      prefix='business_hours_form_'+DAYS[i])
                                   for i in len(DAYS)]

        if (business_form.is_valid() and business_category_form.is_valid() and phone_form.is_valid() and
            businss_details_form.is_valid() and business_payment_options_form.is_valid() and business_hours_form.is_valid()):

            business_name   = business_form.cleaned_data['name']
            address_1       = business_form.cleaned_data['address1']
            address_2       = business_form.cleaned_data['address2']
            address_city    = business_form.cleaned_data['city']
            address_province = business_form.cleaned_data['province']
            address_country = business_form.cleaned_data['country']
            # TODO: zipcode should be found in zipcode table
            address_zipcode = business_form.cleaned_data['zipcode']

            category        = business_category_form.cleaned_data['category']

            phone           = phone_form.cleaned_data['phone']

            payment_cash    = business_payment_options_form.cleaned_data['cash']
            payment_credit_card = business_payment_options_form.cleaned_data['credit_card']
            payment_debit_card = business_payment_options_form.cleaned_data['debit_card']
            payment_cheque    = business_payment_options_form.cleaned_data['cheque']
            payment_gift_cert = business_payment_options_form.cleaned_data['gift_cert']
            payment_others    = business_payment_options_form.cleaned_data['others']



            # TODO: catch possible exceptions here
            try:
                business = Business(name=business_name,address1=address_1, address2=address_2,
                                    city=address_city, province=address_province,
                                    country=address_country)
                business.save()

                phone   = Phone(phone=phone, business=business)
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
    else:
        business_form   = BusinessForm()
        business_category_form = BusinessCategoryForm()
        phone_form      = PhoneForm()
        business_details_form = BusinessDetailsForm()
        business_payment_options_form = BusinessPaymentOptionsForm()
        business_hours_form = BusinessHoursForm(initial={'day':'mon'})
        business_category_form_list = [BusinessCategoryForm(prefix='business_category_form_'+str(i))
                                       for i in range(5)]
        business_hours_form_list = [BusinessHoursForm(initial={'day':i[0]},
                                                      prefix='business_hours_form_'+i[0])
                                   for i in DAYS]
    data = {
        "business_form": business_form,
        "business_category_form": business_category_form,
        "phone_form": phone_form,
        "business_details_form": business_details_form,
        "business_payment_options_form": business_payment_options_form,
        "business_hours_form": business_hours_form,
        "business_category_form_list": business_category_form_list,
        "business_hours_form_list": business_hours_form_list,
        "success": success,
        "error": error
    }
    
    '''
    Check if save thru AJAX or normal POST
    '''
    if(success):
        if request.is_ajax():
            results = {"status":"success", "message":"Business saved."}
            data = json.dumps(results)
            return HttpResponse(data)
        else:
            return render_to_response("business/business_add.html",
                              data, context_instance=RequestContext(request))
    else:
        if request.is_ajax():
            data = json.dumps({"status":"failed", "error":error, "data":request.POST})
            return HttpResponse(data)
        else:
            return render_to_response("business/business_add.html",
                              data, context_instance=RequestContext(request))
