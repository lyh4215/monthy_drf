from .base import *
import os
from dotenv import load_dotenv

load_dotenv(override=True)

ALLOWED_HOSTS = ['localhost']
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('CLOUD_SQL_NAME'),
        'USER': os.getenv('CLOUD_SQL_USER'),
        'PASSWORD': os.getenv('CLOUD_SQL_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
