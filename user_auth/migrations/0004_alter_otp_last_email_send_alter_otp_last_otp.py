# Generated by Django 4.2.6 on 2024-01-04 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0003_otp_attempt_level_otp_attempt_remain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='last_email_send',
            field=models.IntegerField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='otp',
            name='last_otp',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
