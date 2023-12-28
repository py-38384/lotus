import os
"""
Django settings for mycart project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config( 
  cloud_name = "do2afaasp", 
  api_key = "723866855757829", 
  api_secret = "KvF-BG5fagy-fHln_h81liY9Q-0"
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hdoyt4cmxtcx)vz60ua%)+m)+$h0=zs9u1w+mh07w*!%h@6po@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.vercel.app', '.now.sh', '127.0.0.1', 'localhost', 'lotus-7pwc.onrender.com']

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django_apscheduler',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'user_auth.apps.UserAuthConfig',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
]

AUTH_USER_MODEL = 'user_auth.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'mycart.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.total_cart_items',
                'core.context_processors.category',
                'core.context_processors.get_user_info',
                'core.context_processors.subscribe_newsletter',
            ],
        },
    },
]

WSGI_APPLICATION = 'mycart.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'g2e44DE1eb444a653ad2ED6cFbgdg*2f',
        'HOST': 'viaduct.proxy.rlwy.net',
        'PORT': '55426',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Ima ges)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

APSCHEDULER_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

EMAIL_BACKEND=  "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'WorkWithPiyal@gmail.com' 
EMAIL_HOST_PASSWORD = 'wrgp kqoh cqtq hagv'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_FILE_PATH = BASE_DIR / "sent_emails"

# user define grobal variable
PRODUCT_NAME_LIMIT = 15
SHIPPING_CHARGE = 10
DEFAULT_PRODUCT_LIMIT_PER_PAGE = 20
REVIEW_SHOW_LIMIT = 5
PRODUCT_NAME_LIMIT = 25

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'EMAIL_AUTHENTICATION': True,
        'APP': {
            'client_id': '383616365376-177in9c4m8hkjm8he9aup6ff6fllq6l3.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT=True
ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_CHANGE_EMAIL=True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
LOGIN_REDIRECT_URL = "home"
