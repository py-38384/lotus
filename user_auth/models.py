from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    bio = models.TextField(blank=True,null=True)
    mobile_number = models.CharField(max_length=30,blank=True,null=True)

    display_picture = CloudinaryField('image')