# Generated by Django 4.2.6 on 2024-04-03 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_category_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category/'),
        ),
        migrations.AlterField(
            model_name='landingpagerelateddata',
            name='hero_banner',
            field=models.ImageField(blank=True, null=True, upload_to='landingPageRelatedData/'),
        ),
        migrations.AlterField(
            model_name='landingpagerelateddata',
            name='hero_banner_2',
            field=models.ImageField(blank=True, null=True, upload_to='landingPageRelatedData/'),
        ),
        migrations.AlterField(
            model_name='landingpagerelateddata',
            name='hero_banner_20',
            field=models.ImageField(blank=True, null=True, upload_to='landingPageRelatedData/'),
        ),
        migrations.AlterField(
            model_name='landingpagerelateddata',
            name='hero_banner_3',
            field=models.ImageField(blank=True, null=True, upload_to='landingPageRelatedData/'),
        ),
        migrations.AlterField(
            model_name='landingpagerelateddata',
            name='hero_banner_40',
            field=models.ImageField(blank=True, null=True, upload_to='landingPageRelatedData/'),
        ),
        migrations.AlterField(
            model_name='productimages',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='productImages/'),
        ),
        migrations.AlterField(
            model_name='vendorimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='VendorImage/'),
        ),
    ]
