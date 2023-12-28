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
    first_name = models.CharField(max_length=130, null=True, blank=True)
    last_name = models.CharField(max_length=130, null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    primary_address = models.CharField(max_length=200,null=True, blank=True)
    secondary_address = models.CharField(max_length=200,null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=200, null=True)
    small_desc = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="category_image/",null=True,blank=True)
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
    price = models.DecimalField(null=True, max_digits=15, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    small_desc = models.CharField(max_length=255,null=True, blank=False)
    desc = models.TextField(null=True, blank=False)
    add_info = models.TextField(null=True, blank=False)
    digital = models.BooleanField(default=False, null=True, blank=False)
    has_size = models.BooleanField()
    discount = models.IntegerField(blank=True,null=True)
    discount_price = models.IntegerField(blank=True,null=True)
    colors = models.ManyToManyField(Color,blank=True,null=True)
    is_featured = models.BooleanField(blank=True,null=True)
    todays_deals = models.BooleanField(blank=True,null=True)
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
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    color = models.CharField(max_length=200,blank=True,null=True)
    size = models.CharField(max_length=200,blank=True,null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    Customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)
    

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
