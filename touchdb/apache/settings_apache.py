from touchdb.settings import *

# DEBUG configuration

DEBUG = False
TEMPLATE_DEBUG = False

# HOSTS

ALLOWED_HOSTS = ['62.75.188.101', 'www.rollball.net', 'rollball.net']

# LOGGING configuration

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s {%(filename)s:%(lineno)d} [%(levelname)s] %(name)s: %(message)s'
                    },
            },
    'handlers': {
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/home/django/logs/mylog.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
                    },
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/home/django/logs/django_request.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
                    },
            },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
                    },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
                    },
            }
    }
