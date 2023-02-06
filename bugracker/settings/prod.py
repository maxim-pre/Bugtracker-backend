import os
from .common import *
import dj_database_url

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ["bugtracker-prod.herokuapp.com"]

DATABASES = {
    'default': dj_database_url.config()
}
