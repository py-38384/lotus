from apscheduler.schedulers.background import BackgroundScheduler
from .models import Product
from .email.send_email import send_email
from django.conf import settings
from .models import *
import random
import os


def set_todays_deals():
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
    
def order_notify_email_admin():
    if Order.objects.filter(new=True).exists():
        email_body = '<div style="border:1px solid #c9c9c9;">'
        all_new_orders = list(Order.objects.filter(new=True))
        if len(all_new_orders) > 1:
            email_body += '<h2 style="color:#444A4F;margin-left:5px;">You have {0} new orders.</h2><br>'.format(len(all_new_orders))
        else:
            email_body += '<h2 style="color:#444A4F;margin-left:5px;">You have {0} new order.</h2><br>'.format(len(all_new_orders))
        for new_order in all_new_orders:
            all_new_orders_for_this_customer = list(Order.objects.filter(new=True,customer=new_order.customer))
            email_body += '<div style="border-top:1px solid #c9c9c9;padding:7px 5px;font-size:22px;color:#444A4F;"><b style="color:#FC96DA;">({0})</b> new order from <span style="color:#FC96DA;">{1}</span></div>'.format(len(all_new_orders_for_this_customer),new_order.customer.user.username)
        email_body+='</div><br><a href="{0}/orders/" style="color:#FC96DA;font-size:18px;">See orders</a>'.format(os.environ.get('DOMIN'))
        email_body+='<div style="font-size:18px;color:#444A4F;">From lotus..</div>'
        print(email_body)
        email_result = send_email(
            sender_email=os.environ.get('PRIMARY_EMAIL'),
            receiver_email=os.environ.get('SECONDARY_EMAIL'),
            sender_account_pass=os.environ.get('PRIMARY_EMAIL_PASSWORD'),
            mail_subject='Congratulations!! New order Placed.',
            email_body=email_body
        )
        if email_result == True:
            print('New Order email sending successful to the admin.')
        else:
            print(email_result)


def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(update_something, 'interval', seconds=10)
    # scheduler.add_job(update_something, 'cron', second='*/10')
    scheduler.add_job(set_todays_deals, 'cron', hour=1)
    scheduler.add_job(order_notify_email_admin, 'interval', hours=6)
    scheduler.start()