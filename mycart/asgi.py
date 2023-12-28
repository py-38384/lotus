"""
ASGI config for mycart project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycart.settings')

application = get_asgi_application()

import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config( 
  cloud_name = "do2afaasp", 
  api_key = "723866855757829", 
  api_secret = "KvF-BG5fagy-fHln_h81liY9Q-0"
)