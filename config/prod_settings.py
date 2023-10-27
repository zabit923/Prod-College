import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-3_5c*$x(2z%ysdsrfiidfgvj934u38df78*(k-7o=-effqvckox8=gbsg2z&#'


DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'DGU2',
        'USER': 'postgres',
        'PASSWORD': 'Abusik19',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# STATIC_DIR = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')