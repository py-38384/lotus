# Generated by Django 4.2.6 on 2024-04-03 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_alter_user_display_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='display_picture',
            field=models.ImageField(blank=True, null=True, upload_to='user/'),
        ),
    ]