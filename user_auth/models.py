from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    bio = models.TextField(blank=True,null=True)
    mobile_number = models.CharField(max_length=30,blank=True,null=True)

    display_picture = models.ImageField(upload_to="user_auth/display_picture/",null=True,blank=True)
    # display_picture = CloudinaryField('image')

class Email_Verified(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,)
    email_verified = models.BooleanField(default=False,blank=True,null=True)
    last_otp = models.CharField(max_length=60,blank=True,null=True)
    last_email_send = models.IntegerField(blank=True, null=True)
    last_otp_input_time = models.IntegerField(blank=True, null=True)
    otp_input_blocked = models.BooleanField(default=False,blank=True,null=True)
    attempt_remain = models.IntegerField(blank=True, null=True)
    email_attempt_level = models.IntegerField(blank=True, null=True)
    otp_attempt_level = models.IntegerField(blank=True, null=True)
    blocked = models.BooleanField(default=False,blank=True,null=True)