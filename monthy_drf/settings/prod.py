from .base import *
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler, setup_logging
client = google.cloud.logging.Client()
cloud_handler = CloudLoggingHandler(client)

ALLOWED_HOSTS = ['api.monthy-api.com', '34.64.209.29', '.pythonanywhere.com']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
        },
        'cloud': {
            'level': 'INFO',
            'class': 'google.cloud.logging.handlers.CloudLoggingHandler',
            'client': client,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['cloud', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['cloud', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'monthy_drf.middleware.RequestLoggingMiddleware',
]