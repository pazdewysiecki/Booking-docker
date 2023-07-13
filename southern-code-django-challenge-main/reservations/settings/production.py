from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['southern-code-209567a92b6f.herokuapp.com']


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'heroku_10119fcf9d1a57a',
        'USER': 'bb1a0f45c409ee',
        'PASSWORD': '3675ab36',
        'HOST': 'us-cdbr-east-06.cleardb.net',
        'PORT': '3306',
        'OPTIONS': {
        'sql_mode': 'traditional',
            }
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
