from django.db import models
from django.contrib.auth.models import User
from user_auth.models import User as Auth_User
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from decimal import Decimal
from django.utils import timesince
from cloudinary.models import CloudinaryField
from PIL import Image


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=130, null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200,null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=200, null=True)
    small_desc = models.CharField(max_length=255, null=True, blank=True)
    image = CloudinaryField('image')

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100,null=True)
    rgb = models.CharField(max_length=100,blank=True,null=True)
    hex_code = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(null=True, max_digits=15, decimal_places=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    small_desc = models.CharField(max_length=255,null=True, blank=False)
    desc = models.TextField(null=True, blank=False)
    add_info = models.TextField(null=True, blank=False)
    digital = models.BooleanField(default=False, null=True, blank=False)
    has_size = models.BooleanField(default=False)
    discount = models.IntegerField(blank=True,null=True)
    discount_price = models.IntegerField(blank=True,null=True)
    colors = models.ManyToManyField(Color,blank=True,null=True)
    is_featured = models.BooleanField(default=False)
    stock = models.IntegerField(blank=True,null=True)
    todays_deals = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

    @property
    def get_title(self):
        name = self.name
        i = settings.PRODUCT_NAME_LIMIT
        if len(name) > i:
            return name[0:i]+'. . .'
        return name


class ProductImages(models.Model):
    product = models.ForeignKey(Product,blank=True,null=True,default=None,on_delete=models.CASCADE)
    image = CloudinaryField('image')

    def __str__(self):
        return self.product.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True) 
    user = models.ForeignKey(Auth_User, on_delete=models.CASCADE,null=True,blank=True)
    comment = models.TextField(null=True,blank=True)
    review_star = models.IntegerField(null=True,blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[0:30]
    
    @property
    def timesince(self):
        return timesince.timesince(self.time)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    customer_order_no = models.IntegerField(default=1,null=True,blank=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    new = models.BooleanField(default=True)
    registered = models.BooleanField(default=False)
    processing = models.BooleanField(default=False)
    on_your_way = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=100, null=True, blank=True)
    paid = models.BooleanField(default=False,blank=True,null=True)
    notes = models.CharField(max_length=200,blank=True,null=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str('{0}s {1}th order'.format(self.customer.user.username,self.customer_order_no))
    
    @property
    def timesince(self):
        return timesince.timesince(self.date_orderd)

    class Meta:
        ordering = ['-id']

    
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str('{0}`s cart'.format(self.user.username))

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    color = models.CharField(max_length=200,blank=True,null=True)
    size = models.CharField(max_length=200,blank=True,null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str('{0} => {1} '.format(self.product.name,self.quantity))

    @property
    def total(self):
        total = self.product.price * self.quantity
        return total


class ShippingDetails(models.Model):
    Customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    full_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    mobile_number = models.CharField(max_length=30, null=True)
    primary_address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    district = models.CharField(max_length=200, null=True)
    province = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.primary_address)
    
    class Meta:
        ordering = ['-id']
    

class ContactUs(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=250)
    message = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.time_created)
    

class EmailList(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=20,blank=True,null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.email)
    
class LandingPageRelatedData(models.Model):
    hero_banner = CloudinaryField('image')
    hero_title = models.CharField(max_length=30,blank=True,null=True)
    hero_desc = models.CharField(max_length=300,blank=True,null=True)
    hero_button_text = models.CharField(max_length=100,default='Click Here',blank=True,null=True)
    hero_button_link = models.CharField(max_length=500,blank=True,null=True)
    hero_banner_2 = CloudinaryField('image')
    hero_2_title = models.CharField(max_length=30,blank=True,null=True)
    hero_2_desc = models.CharField(max_length=300,blank=True,null=True)
    hero_2_button_text = models.CharField(max_length=100,default='Click Here',blank=True,null=True)
    hero_2_button_link = models.CharField(max_length=500,blank=True,null=True)
    hero_banner_3 = CloudinaryField('image')
    hero_3_title = models.CharField(max_length=30,blank=True,null=True)
    hero_3_desc = models.CharField(max_length=300,blank=True,null=True)
    hero_3_button_text = models.CharField(max_length=100,default='Click Here',blank=True,null=True)
    hero_3_button_link = models.CharField(max_length=500,blank=True,null=True)
    hero_banner_20 = CloudinaryField('image')
    hero_banner_40 = CloudinaryField('image')

    def __str__(self):
        return "Primary Object (this object should be only one)"


class VendorImage(models.Model):
    vendor_name = models.CharField(max_length=100,blank=True,null=True)
    image = CloudinaryField('image')

    def __str__(self):
        if self.vendor_name:
            return str(self.vendor_name)
        return str(self.id)