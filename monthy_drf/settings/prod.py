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
               'level': 'DEBUG',
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
    },
}

setup_logging(cloud_handler)