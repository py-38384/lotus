# Generated by Django 4.2.6 on 2024-01-13 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.cart'),
        ),
    ]
