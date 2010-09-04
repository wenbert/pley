# Create your views here.
from django.http import HttpResponse, Http404
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, redirect
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core import serializers
from django.forms.formsets import formset_factory
from django.core.exceptions import ObjectDoesNotExist

from pley.business.models import *
from pley.review.models import *
from pley.business.forms import *

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

    # Check if user already reviewed this business
    try:
        if request.user.is_authenticated():
            user_review = Review.objects.get(business=business_item, user=request.user, status='A')
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        user_review = None

    print user_review
    ###############
    # Google Maps #
    ###############
    google_apikey   = settings.GOOGLE_MAPS_KEY
    string_location = business_item.address1 +  ', ' +business_item.address2 +  ', ' + business_item.city +  ', ' + business_item.province + ', ' + business_item.country + ', ' + business_item.zipcode
    clean_string_location = ''.join([letter for letter in string_location if not letter.isdigit()])

    urlencoded_string_location = urllib.quote_plus(string_location)

    business_form   = BusinessForm()
    business_category_form = BusinessCategoryForm()
    phone_form      = PhoneForm()
    latlng_form     = BusinessFormSaveLatLng()
    ###############

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
            "latlng_form": latlng_form,
            "phone_form": phone_form,
            "user_review": user_review,
            }
    return render_to_response("business/business_view_v3_localsearch.html",
                              data, context_instance=RequestContext(request))


def business_browse(request):
    #my_objects = get_list_or_404(MyModel, published=True)
    business_list = Business.objects.filter(status='A').order_by('-created_at')
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

@login_required
@transaction.commit_manually
def save_latlng(request, business_id):
    success = False
    error = None
    if request.method == 'POST' and request.is_ajax():
        latlng_form = BusinessFormSaveLatLng(request.POST)
        if(latlng_form.is_valid()):
            try:
                lat  = latlng_form.cleaned_data['lat']
                lng  = latlng_form.cleaned_data['lng']
                
                business = Business.objects.get(id=business_id)
                business.lat = lat
                business.lng = lng
                business.save()
            except IntegrityError, e:
                transaction.rollback()
                success = False
                error = e
                data = json.dumps({"status":"failed", "error": error})
                return HttpResponse(data)
            else:
                transaction.commit()
                success = True
    else:
        data = json.dumps({"status":"failed", "error": "Not POST / AJAX."})
        return HttpResponse(data)
    
    data = json.dumps({"status":"success"})
    return HttpResponse(data)

@login_required
@transaction.commit_manually
def business_add(request):
    success = False
    error = None
    category_count = 1
    detail_count = 1
    CategoriesFormSet = formset_factory(BusinessCategoryForm, extra=category_count, max_num=5)
    HoursFormSet    = formset_factory(BusinessHoursForm, extra=7, max_num=7)
    DetailsFormSet = formset_factory(BusinessDetailsForm, extra=detail_count)

    if request.method == 'POST':
        business_form       = BusinessForm(request.POST)
        hidden_form = HiddenForm(request.POST)
        phone_form     = PhoneForm(request.POST)
        business_payment_options_form = BusinessPaymentOptionsForm(request.POST)

        if hidden_form.is_valid():
            category_count = hidden_form.cleaned_data['category_count']
            detail_count = hidden_form.cleaned_data['detail_count']
            if category_count > 5:
                category_count = 5
        else:
            category_count = 1
            detail_count = 1

        # Business Categories Formset
        categories_formset_additional_data = {
            'form-TOTAL_FORMS': u'%d' % category_count,
            'form-INITIAL_FORMS': u'%d' % category_count,
            'form-MAX_NUM_FORMS': u'5',
        }
        categories_formset = CategoriesFormSet(dict(request.POST.items() + categories_formset_additional_data.items()))

        # Business Hours Formset
        hours_formset_additional_data = {
            'form-TOTAL_FORMS': u'7',
            'form-INITIAL_FORMS': u'7',
            'form-MAX_NUM_FORMS': u'7',
        }
        hours_formset = HoursFormSet(dict(request.POST.items() + hours_formset_additional_data.items()))

        # Business Details Formset
        details_formset_additional_data = {
            'form-TOTAL_FORMS': u'%d' % detail_count,
            'form-INITIAL_FORMS': u'%d' % detail_count,
            'form-MAX_NUM_FORMS': u'',
        }
        details_formset = DetailsFormSet(dict(request.POST.items() + details_formset_additional_data.items()))

        if (business_form.is_valid() and categories_formset.is_valid() and
            phone_form.is_valid() and business_payment_options_form.is_valid() and
            hours_formset.is_valid() and details_formset.is_valid()):

            business_name   = business_form.cleaned_data['name']
            website         = business_form.cleaned_data['website']
            address_1       = business_form.cleaned_data['address1']
            address_2       = business_form.cleaned_data['address2']
            address_city    = business_form.cleaned_data['city']
            address_province = business_form.cleaned_data['province']
            address_country = business_form.cleaned_data['country']
            # TODO: zipcode should be found in zipcode table
            address_zipcode = business_form.cleaned_data['zipcode']
            description     = business_form.cleaned_data['description']

            phone           = phone_form.cleaned_data['phone']
            alt             = phone_form.cleaned_data['alternate']
            fax             = phone_form.cleaned_data['fax']
            mobile          = phone_form.cleaned_data['mobile']

            payment_cash    = business_payment_options_form.cleaned_data['cash']
            payment_credit_card = business_payment_options_form.cleaned_data['credit_card']
            payment_debit_card = business_payment_options_form.cleaned_data['debit_card']
            payment_cheque    = business_payment_options_form.cleaned_data['cheque']
            payment_gift_cert = business_payment_options_form.cleaned_data['gift_cert']
            payment_others    = business_payment_options_form.cleaned_data['others']

            # TODO: catch possible exceptions here
            try:
                print 'saving'
                business = Business(name=business_name,address1=address_1, address2=address_2,
                                    city=address_city, province=address_province,
                                    country=address_country, created_by=request.user,
                                    zipcode=address_zipcode, description=description,
                                    website=website)
                business.save()
                print 'businss saved'

                phone   = Phone(business=business, phone=phone, alternate=alt, fax=fax, mobile=mobile)
                print 'phone created'
                phone.save()
                print 'business and phone saved'
                for category_form in categories_formset.forms:
                    category = category_form.cleaned_data['category']
                    business_category = BusinessCategory(business=business,category=category)
                    business_category.save()
                print 'categories done'
                for hours_form in hours_formset.forms:
                    day = hours_form.cleaned_data['day']
                    open1 = hours_form.cleaned_data['time_open_1']
                    open2 = hours_form.cleaned_data['time_open_2']
                    close1 = hours_form.cleaned_data['time_close_1']
                    close2 = hours_form.cleaned_data['time_close_2']
                    closed = hours_form.cleaned_data['closed']
                    business_hours = BusinessHours(business=business,day=day,time_open_1=open1,time_open_2=open2,
                                                  time_close_1=close1,time_close_2=close2,closed=closed)
                    business_hours.save()
                print 'hours done'
                for detail_form in details_formset.forms:
                    field_name = detail_form.cleaned_data['field_name']
                    field_value = detail_form.cleaned_data['field_value']
                    business_detail = BusinessDetails(business=business,
                                                     field_name=field_name,
                                                     field_value=field_value)
                    business_detail.save()
                print 'details done'
            except IntegrityError, e:
                transaction.rollback()
                success = False
                error = e
                raise e
            else:
                transaction.commit()
                success = True
    else:
        hidden_form = HiddenForm()
        business_form   = BusinessForm()
        categories_formset = CategoriesFormSet()
        phone_form      = PhoneForm()
        business_payment_options_form = BusinessPaymentOptionsForm()
        hidden_form = HiddenForm()
        details_formset = DetailsFormSet()
        initial_days = [
            {'day':u'mon'},
            {'day':u'tue'},
            {'day':u'wed'},
            {'day':u'thu'},
            {'day':u'fri'},
            {'day':u'sat'},
            {'day':u'sun'},
        ]
        hours_formset = HoursFormSet(initial=initial_days)
    data = {
        "business_form": business_form,
        "phone_form": phone_form,
        "business_payment_options_form": business_payment_options_form,
        "hidden_form": hidden_form,
        "categories_formset": categories_formset,
        "hours_formset": hours_formset,
        "details_formset": details_formset,
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
