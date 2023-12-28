from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import forms as core_forms
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Q
from random import randint
from .models import *
from django.conf import settings
from user_auth.models import User
from user_auth import forms
from datetime import datetime
from pathlib import Path
from decimal import Decimal
import json
import os

# Create your views here.

def get_title(name,i):
    if len(name) > i:
        return name[0:i]+'. . .'
    return name

import math

def get_product_array(products):
    product_arr = []
    for product in products:
            product_obj = {}
            product_obj['id'] = product.id
            product_obj['title'] = get_title(product.name,25)
            product_obj['price'] = product.price.normalize()
            product_obj['discount'] = product.discount
            product_obj['review'] = None
            product_obj['comment'] = None
            if product.discount:
                if product.discount>0:
                    product_obj['discount'] = product.discount
                    discount_price_cut = product.price*(Decimal(product.discount)/Decimal(100))
                    discount_price = product.price-discount_price_cut
                    product_obj['price'] = discount_price.normalize()

                    product_obj['original_price'] = product.price.normalize()

            images = list(ProductImages.objects.filter(product=product))
            if len(images) > 0:
                product_obj['image'] = images[0].image
            else:
                product_obj['image'] = False
            product_arr.append(product_obj)
    return product_arr


class Index(View):
    def get(self, request):
        recent_product = []
        categories_arr = [] 
        one_week = 60*60*24*7
        all_products = Product.objects.all()
        products = list(Product.objects.filter(is_featured=True))
        categories = Category.objects.all()

        for category in categories:
            categories_obj = {}
            categories_obj['name'] = category.name
            categories_obj['image'] = category.image
            categories_obj['products'] = len(list(Product.objects.filter(category=category)))
            categories_arr.append(categories_obj)

        featured_products = get_product_array(products)
        
        for product in all_products:
            date_created = product.date_added
            date_created = date_created.replace(tzinfo=None)
            now = datetime.now()
            diff = now - date_created
            diff = diff.total_seconds()
            if(diff < one_week):
                product_obj = {}
                product_obj['id'] = product.id
                product_obj['title'] = get_title(product.name,25)
                product_obj['price'] = product.price.normalize()
                product_obj['review'] = None
                product_obj['comment'] = None
                if product.discount:
                    if product.discount>0:
                        product_obj['discount'] = product.discount
                        discount_price_cut = product.price*(Decimal(product.discount)/100)
                        discount_price = product.price-discount_price_cut
                        product_obj['price'] = discount_price.normalize()
                        product_obj['original_price'] = product.price.normalize()
                images = list(ProductImages.objects.filter(product=product))
                if len(images) > 0:
                    product_obj['image'] = images[0].image
                else:
                    product_obj['image'] = False
                recent_product.append(product_obj)
            
        
        context = {'featured_products':featured_products,'recent_product':recent_product}
        return render(request,"index.html", context)

class UpdateItem(View):
    def post(self, request):
        if request.user.is_authenticated:
            productID = request.POST.get('productID')
            action = request.POST.get('action')
            quantity = request.POST.get('quantity')
            order_item_id = request.POST.get('order_item_id')
            color = request.POST.get('color')
            size = request.POST.get('size')
            quantity = int(quantity)

            total_items = 0
            subtotal = 0
            discount_price_cut = 0
            discount = False

            customer, created = Customer.objects.get_or_create(user=request.user)
            product = Product.objects.get(id=productID)
            order, created = Order.objects.get_or_create(customer=customer,complete=False)
            
            if order_item_id=="undefined":
                order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
                if created:
                    order_item.color = color
                    order_item.size = size
                    order_item.quantity = quantity
                    order_item.save()
                else:
                    order_item.quantity += quantity
                    order_item.save()
                order_item_id = order_item.id

            else:
                order_item_id = int(order_item_id)
                order_item = OrderItem.objects.get(order__customer__user=request.user,id=order_item_id)
                if action == 'add':
                    order_item.quantity = (order_item.quantity+quantity)
                elif action == 'remove':
                    order_item.quantity = (order_item.quantity-quantity)

                order_item.save()
                if order_item.quantity <= 0:
                    order_item.delete()


            items = list(OrderItem.objects.filter(order=order.id))
            for item in items:
                if item.product.discount:
                    if item.product.discount > 0:
                        single_discount_price_cut = item.product.price*(Decimal(product.discount)/Decimal(100))
                        discount_price_cut += single_discount_price_cut*item.quantity
                total_items+=item.quantity
                subtotal+=item.total
            subtotal-=discount_price_cut

            if order_item.product.discount:
                    if order_item.product.discount > 0:
                        discount=True
                        single_discount_price_cut = order_item.product.price*(Decimal(order_item.product.discount)/Decimal(100))
                        order_item_product_discount_price = order_item.product.price-single_discount_price_cut
                        total_price = order_item.quantity*order_item_product_discount_price
                    else:
                        total_price = Decimal(order_item.quantity)*order_item.product.price
            else:
                total_price = order_item.quantity*order_item.product.price

            original_total_price = order_item.quantity*order_item.product.price

            return JsonResponse({'id':order_item_id,'quantity':order_item.quantity,'total_items':total_items,'total_price':total_price.normalize(),'original_total_price':original_total_price.normalize(),'discount':discount,'subtotal':subtotal.normalize(),'total':(subtotal+settings.SHIPPING_CHARGE).normalize()})
        
class Search(View):
    def get(self, request):
        page_list =[]
        q = request.GET.get('q')
        
        page_number = request.GET.get('page')
        if page_number:
            page_number = int(page_number)
        else:
            page_number = 1
        if q:
            try:
                q=int(q)
                products_array = list(Product.objects.filter(id=q))
                q='Product ID: {0}'.format(q)
            except:
                products_array = list(Product.objects.filter(Q(name__icontains=q)|Q(category__name__icontains=q)))
            p = Paginator(products_array,settings.DEFAULT_PRODUCT_LIMIT_PER_PAGE)
        else:
            products_array = list(Product.objects.all())
            q = "All Products"
            p = Paginator(products_array,settings.DEFAULT_PRODUCT_LIMIT_PER_PAGE)
        products = p.get_page(page_number)
        last_page = products.paginator.num_pages

        for i in range(1,last_page+1):
            if (i==(page_number-2)and(page_number-2)>0) or (i==(page_number-1)and(page_number-1)>0) or  (i == page_number and last_page>1) or (i==(page_number+1)and(page_number+1)<=last_page) or (i==(products.number+2)and(products.number+2)<=last_page):
                page_list.append(i)

        product_arr = get_product_array(products)

        context = {'products':product_arr,'pagenator_object':products,'last_page':last_page,'page_list':page_list,'current_page':page_number,'q':q, 'total_product':len(products_array), 'total_inpage_product':len(product_arr)}
        
        return render(request,"search.html", context)

class Deals(View):
    def get(self, request):
        products = list(Product.objects.filter(todays_deals=True))
        context = {'products':get_product_array(products)}
        return render(request,"deals.html", context)


class Shop(View):
    def get(self, request, offset_key=0):
        page_list = []
        try:
            product_limit = int(request.session['limit'])
        except KeyError:
            product_limit = settings.DEFAULT_PRODUCT_LIMIT_PER_PAGE
        limit = request.GET.get('limit')
        if limit:
            request.session['limit'] = limit
            product_limit = int(limit)
        price_range = request.GET.get('price_range')
        price_range_value = {}
        product_ajex_arr = []
        for i in range(7):
            price_range_value[str(i)] = False
        # product_limit = 2
        if price_range:
            if price_range == "0":
                product_ajex_arr.extend(list(Product.objects.all()))
            for c in price_range:
                if int(c) == 1 and '0' not in price_range:
                    price_range_value['1'] = True
                    product_ajex_arr.extend(list(Product.objects.filter(price__gt=0,price__lte=100)))
                if int(c) == 2 and '0' not in price_range:
                    price_range_value['2'] = True
                    product_ajex_arr.extend(list(Product.objects.filter(price__gt=100,price__lte=200)))
                if int(c) == 3 and '0' not in price_range:
                    price_range_value['3'] = True
                    product_ajex_arr.extend(list(Product.objects.filter(price__gt=200,price__lte=300)))
                if int(c) == 4 and '0' not in price_range:
                    price_range_value['4'] = True
                    product_ajex_arr.extend(list(Product.objects.filter(price__gt=300,price__lte=400)))
                if int(c) == 5 and '0' not in price_range:
                    price_range_value['5'] = True
                    product_ajex_arr.extend(list(Product.objects.filter(price__gt=400,price__lte=500)))
                if int(c) == 6 and '0' not in price_range:
                    price_range_value['6'] = True
                    product_ajex_arr.extend(list(Product.objects.filter(price__gt=500)))

            p = Paginator(product_ajex_arr,product_limit)
        else:
            products_all = list(Product.objects.all())
            p = Paginator(products_all,product_limit)
            
        page_number_request = request.GET.get('page')
        if page_number_request:
            page_number = int(page_number_request)
        else:
            page_number = 1

        products = p.get_page(page_number)
        last_page = products.paginator.num_pages
        for i in range(1,last_page+1):
            if (i==(page_number-2)and(page_number-2)>0) or (i==(page_number-1)and(page_number-1)>0) or  (i == page_number and last_page>1) or (i==(page_number+1)and(page_number+1)<=last_page) or (i==(products.number+2)and(products.number+2)<=last_page):
                page_list.append(i)
                

        product_arr = get_product_array(products)

        context = {'products':product_arr,'pagenator_object':products,'last_page':last_page,'page_list':page_list,'current_page':page_number,'price_range':price_range,'price_range_value':price_range_value,}
        if price_range and not page_number_request:
            return render(request,"shop_ajex.html", context)
        else:
            return render(request,"shop.html", context)
    

class Cart(View):
    def get(self, request):
        product_obj = []
        items = []
        subtotal = 0
        if request.user.is_authenticated:
            customer, created = Customer.objects.get_or_create(user=request.user)
            order, created = Order.objects.get_or_create(customer=customer.id, complete=False,)
            items = list(OrderItem.objects.filter(order=order.id))
        else:
            try:
                cart = json.loads(request.COOKIES['cart'])
            except KeyError:
                cart = {}
            for key in cart:
                product = Product.objects.get(id=key)
                product_obj_element = {}
                product_obj_element['id'] = product.id
                product_obj_element['product_id'] = product.id
                if len(product.name) > 30:
                    product_obj_element['title'] = product.name[0:30]+"...."
                else:
                    product_obj_element['title'] = product.name
                product_obj_element['quantity'] = cart[key]['quantity']
                if product.discount:
                    if product.discount > 0:
                        product_obj_element['discount'] = product.discount
                        discount_price_cut = product.price*(Decimal(product.discount)/Decimal(100))
                        discount_price = product.price-discount_price_cut
                        product_obj_element['price'] = discount_price.normalize()
                        product_obj_element['original_price'] = product.price.normalize()
                        product_obj_element['total'] = ((product.price*cart[key]['quantity'])-(discount_price_cut*cart[key]['quantity'])).normalize()
                        product_obj_element['original_total'] = (product.price*cart[key]['quantity']).normalize()
                    else:
                        product_obj_element['total'] = product.price*cart[key]['quantity'].normalize()
                        product_obj_element['price'] = product.price.normalize()
                else:
                    product_obj_element['total'] = product.price*cart[key]['quantity'].normalize()
                    product_obj_element['price'] = product.price.normalize()
                image_obj = list(ProductImages.objects.filter(product=product))
                if image_obj:
                    product_obj_element['image'] = image_obj[0].image
                else:
                    product_obj_element['image'] = None
                subtotal+=product_obj_element['total']
                product_obj.append(product_obj_element)


        for item in items:
            product_obj_element = {}
            product_obj_element['id'] = item.id
            product_obj_element['product_id'] = item.product.id
            if len(item.product.name) > 30:
                product_obj_element['title'] = item.product.name[0:30]+"...."
            else:
                product_obj_element['title'] = item.product.name
            product_obj_element['quantity'] = item.quantity
            if item.product.discount:
                if item.product.discount > 0:
                    product_obj_element['discount'] = item.product.discount
                    discount_price_cut = item.product.price*(Decimal(item.product.discount)/Decimal(100))
                    discount_price = item.product.price-discount_price_cut
                    product_obj_element['price'] = discount_price.normalize()
                    product_obj_element['original_price'] = item.product.price.normalize()
                    product_obj_element['total'] = item.total-(discount_price_cut*item.quantity).normalize()
                    product_obj_element['original_total'] = item.total.normalize()
                else:
                    product_obj_element['total'] = item.total.normalize()
                    product_obj_element['price'] = item.product.price.normalize()
            else:
                product_obj_element['total'] = item.total.normalize()
                product_obj_element['price'] = item.product.price.normalize()
            image_obj = list(ProductImages.objects.filter(product=item.product))
            if image_obj:
                product_obj_element['image'] = image_obj[0].image
            else:
                product_obj_element['image'] = None
            subtotal+=product_obj_element['total']
            product_obj.append(product_obj_element)

        subtotal = subtotal
        context = {'product_obj':product_obj, 'subtotal':subtotal, 'shipping':settings.SHIPPING_CHARGE, 'total':subtotal+settings.SHIPPING_CHARGE }
        return render(request,'cart.html',context)

class Order_Item_Delete(View):
    def get(self, request, productid):
        order_item = OrderItem.objects.get(id=productid)
        if order_item.order.customer.user == request.user:
            order_item.delete()
            return JsonResponse('Order item deleted',safe=False)
        else:
            return JsonResponse('You are not authorized to do that!!',safe=False)
        

class Checkout(View):
    def get(self, request):
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            order, created = Order.objects.get_or_create(customer=customer, complete=False,)
            items = list(OrderItem.objects.filter(order=order.id))
        else:
            messages.warning(request,'You must login to continue')
            return redirect('login')
        subtotal = Decimal(0)
        shipping = Decimal(settings.SHIPPING_CHARGE)
        for item in items:
            subtotal+=Decimal(item.total)
        total = subtotal+shipping
        context = {'customer':customer,'items':items, 'subtotal':subtotal, 'shipping':shipping, 'total':total}
        return render(request,"checkout.html", context)
    

class Contact(View):
    def get(self, request):
        form = core_forms.ContactUsForm()
        context = {'form':form}
        return render(request,"contact.html", context)
    
    def post(self, request):
        form = core_forms.ContactUsForm(request.POST)
        if form.is_valid():
            new_form = core_forms.ContactUsForm()
            context = {'form':new_form}
            messages.success(request,'<strong>Your message has been submited</strong> soon we will contact you.')
            form.save()
            return render(request,"contact.html", context)
        else:
            context = {'form':form} 
            return render(request,"contact.html", context)
    

class About(View):
    def get(self, request):
        context = {}
        return render(request,"about.html", context)
    

class Detail(View):
    def get(self, request, id):
        context = {}
        related_product_array = []
        product_image_obj = {}
        has_order = False
        product = Product.objects.get(id=id)
        related_products = list(Product.objects.filter(category=product.category))[:10]
        reviews_all = list(Review.objects.filter(product=product).order_by('-time'))
        review_all_length = len(reviews_all)
        p = Paginator(reviews_all,settings.REVIEW_SHOW_LIMIT)
        reviews = p.get_page(1)
        last_page = reviews.paginator.num_pages
        order_items = OrderItem.objects.all()
        has_size = product.has_size
        colors = product.colors.all()

        for order_item in order_items:
            if order_item.order.customer.user == request.user and order_item.product == product:
                has_order = True
                break

        images = list(ProductImages.objects.filter(product=product))
        if images:
            hero_image = images[0]
            context = {'product':product,'images':images[1:],'hero_image':hero_image}
        else:
            context = {'product':product,'related_products':related_products}
            
        for related_product in related_products:
            if product.id != related_product.id:
                product_image_obj = {}
                product_image_obj['id'] = related_product.id
                product_image_obj['title'] = get_title(related_product.name,20)
                product_image_obj['price'] = related_product.price
                product_image_obj['reviews'] = list[Review.objects.filter(product=product)]
                if related_product.discount:
                    if not related_product.discount==0:
                        product_image_obj['discount'] = related_product.discount
                        discount_price_cut = related_product.price*(Decimal(related_product.discount)/Decimal(100))
                        discount_price = related_product.price-discount_price_cut
                        product_image_obj['price'] = discount_price
                        product_image_obj['original_price'] = related_product.price
                image_obj = list(ProductImages.objects.filter(product=related_product))
                if image_obj:
                    product_image_obj['image'] = image_obj[0].image
                else:
                    product_image_obj['image'] = None
                related_product_array.append(product_image_obj)

        context['related_products_array'] = related_product_array
        context['has_order'] = has_order
        context['colors'] = colors
        context['has_size'] = has_size
        context['reviews'] = reviews
        context['review_last_page'] = last_page
        context['review_all_length'] = review_all_length
        if product.discount:
                if not product.discount==0:
                    discount_price_cut = product.price*(Decimal(product.discount)/Decimal(100))
                    discount_price = product.price-discount_price_cut
                    context['discount_price'] =  discount_price
        return render(request,"detail.html", context)
    

class AddReview(View):
    def post(self, request):
        if request.user.is_authenticated:
            try:
                review_arr = []
                display_picture_url = ''
                user = request.user
                comment = request.POST.get('comment')
                review_star = request.POST.get('review_star')
                review_id = request.POST.get('review_id')
                if review_id:
                    review_model_obj = Review.objects.get(id=review_id)
                    product = Product.objects.get(id=review_model_obj.product.id)
                    review_model_obj.comment = comment
                    review_model_obj.review_star = review_star
                    review_model_obj.save()
                else:
                    product_id = request.POST.get('product_id')
                    product = Product.objects.get(id=product_id)
                    review_model_obj = Review(product=product,user=user,comment=comment,review_star=review_star)
                    review_model_obj.save()
                review_all = list(Review.objects.filter(product=product).order_by('-time'))
                review_all_length = len(review_all)
                p = Paginator(review_all,settings.REVIEW_SHOW_LIMIT)
                reviews = p.get_page(1)
                last_page = reviews.paginator.num_pages
                for review in reviews:
                    if review.user.display_picture:
                        display_picture_url = review.user.display_picture.url
                    else:
                        display_picture_url = '/static/img/review_default_user_dp.png'
                        
                    review_obj = {}
                    review_obj['id'] = review.id
                    review_obj['user'] = {'user_name':review.user.username,'user_id':review.user.id,'user_image':display_picture_url,'user_email':review.user.email}
                    review_obj['comment'] = review.comment
                    review_obj['review_star'] = review.review_star
                    review_obj['time'] = review.time
                    review_obj['timesince'] = review.timesince
                    review_arr.append(review_obj)
                return JsonResponse({'reviews':review_arr,'product':product.name,'product_count':review_all_length,'last_page':last_page})
            except Exception as e:
                print(e)
                return JsonResponse({"error": "Something terrible happened.."})
        else:
            return redirect('home')
        

class AddReviewForAccountManage(View):
    def post(self, request):
        if request.user.is_authenticated:
            try:
                review_arr = []
                product_arr = []
                comment = request.POST.get('comment')
                review_star = request.POST.get('review_star')
                review_id = request.POST.get('review_id')
                review_model_obj = Review.objects.get(id=review_id)
                product = Product.objects.get(id=review_model_obj.product.id)
                review_model_obj.comment = comment
                review_model_obj.review_star = review_star
                review_model_obj.save()
                reviews = list(Review.objects.filter(user=request.user).order_by('-time'))
                for review in reviews:
                    if not review.product in product_arr:
                        product_arr.append(review.product)
                for product in product_arr:
                    related_product_reviews_obj = {'product_name':product.name}
                    related_product_reviews = list(Review.objects.filter(product=product,user=request.user).order_by('-time'))
                    related_product_reviews_obj['list'] = related_product_reviews
                    review_arr.append(related_product_reviews_obj)
                context = {'review_arr':review_arr}
                return render(request,"yourreviews_ajex.html",context)
            except Exception as e:
                print(e)
                return JsonResponse({"error": "Something terrible happened.."})
        else:
            return redirect('home')


class DeleteReview(View):
    def post(self, request):
        if request.user.is_authenticated:
            id = request.POST.get('review_id')
            review = Review.objects.get(id=id)
            if request.user == review.user:
                product = Product.objects.get(id=review.product.id)
                review.delete()
                review_all = list(Review.objects.filter(product=product))
                review_count = len(review_all)
                return JsonResponse({'success':'Review deleted sucessfully..','total_review':review_count,'product':product.name})
            else:
                return JsonResponse({"error": "ERROR!! Your are not the owner of this review. don't try to fool me.."})
        else:
            return redirect('home')


class GetReview(View):
    def post(self, request):
        if request.user.is_authenticated:
            try:
                review_id = request.POST.get('review_id')
                review = Review.objects.get(id=review_id)
                if request.user == review.user:
                    return JsonResponse({'product':review.product.id,'user':review.user.id,'review_star':review.review_star,'comment':review.comment,'time':review.time})
                else:
                    return JsonResponse({"error": "ERROR!! Your are not the owner of this review. don't try to fool me.."})
            except Exception as e:
                print(e)
                return JsonResponse({"error": "ERROR!! most probably review id wrong."})
        else:
            return redirect('home')


class GetReviews(View):
    def post(self, request):
        review_arr = []
        page = request.POST.get('review_page_indicator')
        id = request.POST.get('product_id')
        product = Product.objects.get(id=id)
        review_all = list(Review.objects.filter(product=product).order_by('-time'))
        review_count = len(review_all)
        p = Paginator(review_all,settings.REVIEW_SHOW_LIMIT)
        reviews = p.get_page(page)
        last_page = reviews.paginator.num_pages
        for review in reviews:
            if review.user.display_picture:
                display_picture_url = review.user.display_picture.url
            else:
                display_picture_url = '/static/img/review_default_user_dp.png'
                
            review_obj = {}
            review_obj['id'] = review.id
            review_obj['user'] = {'user_name':review.user.name,'user_id':review.user.id,'user_image':display_picture_url,'user_email':review.user.email}
            review_obj['comment'] = review.comment
            review_obj['review_star'] = review.review_star
            review_obj['time'] = review.time
            review_obj['timesince'] = review.timesince
            review_arr.append(review_obj)
        return JsonResponse({'reviews':review_arr,'product':product.name,'last_page':last_page,'product_count':review_count})


class Offer(View):
    def get(self, request, keyword):
        product_arr = []
        page_list =[]
        products = Product.objects.filter(category__name=keyword)
        if products:
            page_number_request = request.GET.get('page')
            if page_number_request:
                page_number = int(page_number_request)
            else:
                page_number = 1

            p = Paginator(products,settings.DEFAULT_PRODUCT_LIMIT_PER_PAGE)
            products = p.get_page(page_number)
            last_page = products.paginator.num_pages
            for i in range(1,last_page+1):
                if (i==(page_number-2)and(page_number-2)>0) or (i==(page_number-1)and(page_number-1)>0) or  (i == page_number and last_page>1) or (i==(page_number+1)and(page_number+1)<=last_page) or (i==(products.number+2)and(products.number+2)<=last_page):
                    page_list.append(i)

            product_arr = get_product_array(products)
            
            context = {'products':product_arr,'pagenator_object':products,'last_page':last_page,'page_list':page_list,'current_page':page_number,'keyword':keyword}
            return render(request,"offer.html", context)
        else:
            return redirect('shop')
              

class Discount(View):
    def get(self, request, keyword):
        product_arr = []
        page_list =[]
        if keyword=='20':
            products = Product.objects.filter(discount__gte=keyword,discount__lt=40)
        elif keyword=='40':
            products = Product.objects.filter(discount__gte=keyword)
        else:
            return redirect('shop')
        
        page_number_request = request.GET.get('page')
        if page_number_request:
            page_number = int(page_number_request)
        else:
            page_number = 1

        p = Paginator(products,settings.DEFAULT_PRODUCT_LIMIT_PER_PAGE)
        products = p.get_page(page_number)
        last_page = products.paginator.num_pages
        for i in range(1,last_page+1):
            if (i==(page_number-2)and(page_number-2)>0) or (i==(page_number-1)and(page_number-1)>0) or  (i == page_number and last_page>1) or (i==(page_number+1)and(page_number+1)<=last_page) or (i==(products.number+2)and(products.number+2)<=last_page):
                page_list.append(i)

        product_arr = get_product_array(products)

        
        context = {'products':product_arr,'pagenator_object':products,'last_page':last_page,'page_list':page_list,'current_page':page_number,'keyword':keyword}
        return render(request,"discount.html", context)
    

class ManageAccount(View):
    def get(self,request):
        context = {}
        return render(request,"manage.html",context)
    

class CustomizeProfile(View):
    def get(self,request):
        user = User.objects.get(id=request.user.id)
        form = forms.ProfileCostomize(instance=user)
        context = {'form':form}
        return render(request,"customize.html",context)
    
    def post(self,request):
        user = User.objects.get(id=request.user.id)
        form = forms.ProfileCostomize(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,'<strong>Profile update successfully</strong>...')
            return redirect('customize_profile')
        else:
            context = {'form':form}
            return render(request,"customize.html",context) 
    

class LoginSecurity(View):
    def get(self,request):
        context = {}
        return render(request,"loginsecurity.html",context)
    

class ChangePassword(View):
    def get(self,request):
        context = {}
        user = User.objects.get(id=request.user.id)
        form = core_forms.ChangePasswordForm(user)
        context['form'] = form
        return render(request,"change_password.html",context)
    
    def post(self,request):
        context = {}
        user = User.objects.get(id=request.user.id)
        email = user.email
        form = core_forms.ChangePasswordForm(user,request.POST)
        if form.is_valid():
            password = form.cleaned_data['new_password1']
            form.save()
            login(request,user)
            messages.success(request,'Password change successful...')
            return redirect('change_password')
        else:
            context['form'] = form
            return render(request,"change_password.html",context)

class ChangeEmail(View):
    def get(self,request):
        if user.socialaccount_set.exists():
            return redirect('login_security')
        else:   
            user = User.objects.get(id=request.user.id)
            email = user.email
            context = {'email':email}
            return render(request,"change_email.html",context)
        
    def post(self,request):
        if user.socialaccount_set.exists():
            return redirect('home')
        else:
            context = {}
            try:
                new_email = request.POST['new_email']
                if User.objects.filter(email=new_email).exists():
                    context = {'email':new_email}
                    messages.error(request,'This email is already exist!!')
                    return render(request,"change_email.html",context)
                else:
                    context = {'email':new_email}
                    user = User.objects.get(id=request.user.id)
                    user.email = new_email
                    user.save()
                    messages.success(request,'Email change successful...')
                    return render(request,"change_email.html",context)
            except:
                pass


class YourReviews(View):
    def get(self,request):
        review_arr = []
        product_arr = []
        reviews = list(Review.objects.filter(user=request.user).order_by('-time'))
        for review in reviews:
            if not review.product in product_arr:
                product_arr.append(review.product)
        for product in product_arr:
            related_product_reviews_obj = {'product_name':product.name}
            related_product_reviews = list(Review.objects.filter(product=product,user=request.user).order_by('-time'))
            related_product_reviews_obj['list'] = related_product_reviews
            review_arr.append(related_product_reviews_obj)
        context = {'review_arr':review_arr}
        return render(request,"yourreviews.html",context)


class YourOrder(View):
    def get(self, request):
        context = {}
        return render(request,"yourorder.html",context)
    
class Subscribe(View):
    def post(self, request):
        form = core_forms.SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Email successfully recoded...')
            return redirect('home')
        else:
            messages.error(request,form.errors['email'])
            return redirect('home')
