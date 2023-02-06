from .common import *


DEBUG = True

SECRET_KEY = 'django-insecure-+k-3=6@0h82#0tnoe5c%h#8px==d=+ay@goo_wrd7-(4_$&tsn'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bugtracker',
        'USER': 'root',
        'HOST': 'localhost',
        'PASSWORD': 'mp140401',

    }
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000'
]