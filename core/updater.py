from apscheduler.schedulers.background import BackgroundScheduler
from .models import Product
from django.conf import settings
import random


def update_something():
    products = list(Product.objects.all())
    for product in products:
        product.todays_deals = False
        product.save()
    random_products = random.sample(products, settings.DEFAULT_PRODUCT_LIMIT_PER_PAGE)
    # if you want only a single random item
    # random_item = random.choice(items)
    for random_product in random_products:
        random_product.todays_deals = True
        random_product.save()

def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(update_something, 'interval', seconds=10)
    # scheduler.add_job(update_something, 'cron', second='*/10')
    scheduler.add_job(update_something, 'cron', hour=1)
    scheduler.start()