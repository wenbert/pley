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

def business_browse(request):
    #my_objects = get_list_or_404(MyModel, published=True)
    business_list = Business.objects.all().order_by('-created_at')
    if not business_list:
        raise Http404
        
    paginator = Paginator(business_list, 3)
    
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    
    try:
        businesses = paginator.page(page)
    except (EmptyPage, InvalidPage):
        businesses = paginator.page(paginator.num_page)
        
    data = {"string": "value",
            "business_list": business_list,
            "businesses": businesses,}
    return render_to_response("business/business_browse.html",
                              data, context_instance=RequestContext(request))

def business_view(request, business_id):
    business_item = Business.objects.select_related().get(id=business_id)
    address_list = Address.objects.filter(business=business_item)
    
    data = {"business_item": business_item,
            "address_list": address_list}
    return render_to_response("business/business_view.html",
                              data, context_instance=RequestContext(request))

@login_required
@transaction.commit_manually
def business_add(request):
    success = False
    error = None
    if request.method == 'POST':
        business_form       = BusinessForm(request.POST)
        address_form        = AddressForm(request.POST)
        business_category_form = BusinessCategoryForm(request.POST)
        phone_form          = PhoneForm(request.POST)
        
        if (business_form.is_valid() and address_form.is_valid() and business_category_form.is_valid() and phone_form.is_valid()):
            
            business_name   = business_form.cleaned_data['name']
            category        = business_category_form.cleaned_data['category']
            address_1       = address_form.cleaned_data['address1']
            address_2       = address_form.cleaned_data['address2']
            address_city    = address_form.cleaned_data['city']
            address_province = address_form.cleaned_data['province']
            address_country = address_form.cleaned_data['country']
            
            phone_number    = phone_form.cleaned_data['phone_number']
            
            # TODO: zipcode should be found in zipcode table
            address_zipcode = address_form.cleaned_data['zipcode']

            # TODO: catch possible exceptions here
            try:
                business = Business(name=business_name)
                business.save()
                                  
                address = Address(address1=address_1, address2=address_2,
                                  city=address_city, province=address_province,
                                  country=address_country,
                                  zipcode=address_zipcode,
                                  business=business)    
                address.save()
                
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
        address_form    = AddressForm()
        business_category_form = BusinessCategoryForm()
        phone_form      = PhoneForm()
        
    data = {
              "business_form": business_form,
              "address_form": address_form,
              "business_category_form": business_category_form,
              "phone_form": phone_form,
              "success": success,
              "error": error
           }
    return render_to_response("business/business_add.html",
                              data, context_instance=RequestContext(request))

