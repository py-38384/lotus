# Generated by Django 4.2.6 on 2024-01-13 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_shippingdetails_order_new_alter_orderitem_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=15, null=True),
        ),
    ]
