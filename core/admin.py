from django.contrib import admin
from .models import *


# admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Color)
admin.site.register(ContactUs)
admin.site.register(EmailList)


class ProductImageAdmin(admin.StackedInline):
    model=ProductImages

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    class Meta:
        model=Product

@admin.register(ProductImages)
class ProductImageAdmin(admin.ModelAdmin):
    pass


