from core.models import *
from core.forms import *
from user_auth.models import User,Email_Verified
from django.shortcuts import render, redirect
from django.conf import settings

def total_cart_items(request):
    total_items=0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = list(OrderItem.objects.filter(cart=cart))
        for item in items:
            total_items+=item.quantity
    return {'total_cart_items':total_items}

def get_user_info(request):
    context = {}
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        context['logged_in_user'] = True
        if user.first_name and user.last_name:
            context['username'] = user.first_name + " " + user.last_name
        else:
            context['username'] = user.username
        if user.display_picture:
            context['image'] = user.display_picture.url 
        else:
            try:
                user.socialaccount_set.exists()
                context['image'] = user.socialaccount_set.all()[0].extra_data['picture']
            except Exception as e:
                context['image'] = '/static/img/user.png'
                
    else:
        context['logged_in_user'] = False
    return context

def category(request):
    categories_arr = [] 
    categories = Category.objects.all()

    for category in categories:
        categories_obj = {}
        categories_obj['name'] = category.name
        categories_obj['image'] = category.image
        categories_obj['products'] = len(list(Product.objects.filter(category=category)))
        categories_arr.append(categories_obj)

    return {'categories':categories_arr,'DEFAULT_PRODUCT_LIMIT_PER_PAGE':settings.DEFAULT_PRODUCT_LIMIT_PER_PAGE}

def subscribe_newsletter(request):
    subscribe_form = SubscribeForm()
    return {'subscribe_form':subscribe_form}

def landing_page_data(request):
    if LandingPageRelatedData.objects.filter(id=1).exists():
        lprd_obj = LandingPageRelatedData.objects.get(id=1)
        vendor_img_obj = list(VendorImage.objects.all())
        print('Debug = {0}'.format(lprd_obj.hero_banner.url))
        return {'lprd_obj':lprd_obj,'vendor_img_obj':vendor_img_obj}
    return {'lprd_obj':{},'vendor_img_obj':[]}