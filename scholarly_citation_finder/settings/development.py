from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'dblp': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DBLP_DATABASE_NAME', 'dblp'),
        'USER': os.getenv('DBLP_DATABASE_USER', 'postgres'),
        'PASSWORD': os.getenv('DBLP_DATABASE_PASSWORD', 'root'),
        'HOST': '127.0.0.1',
        'PORT': '5432'
    },
    'citeseerx': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('CITESEERX_DATABASE_NAME', 'citeseerx'),
        'USER': os.getenv('CITESEERX_DATABASE_USER', 'postgres'),
        'PASSWORD': os.getenv('CITESEERX_DATABASE_PASSWORD', 'root'),
        'HOST': '127.0.0.1',
        'PORT': '5432'
    },
    'mag': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('MAG_DATABASE_NAME', 'mag'),
        'USER': os.getenv('MAG_DATABASE_USER', 'postgres'),
        'PASSWORD': os.getenv('MAG_DATABASE_PASSWORD', 'root'),
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}


# Logging
# http://ianalexandr.com/blog/getting-started-with-django-logging-in-5-minutes.html
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(module)s] %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.abspath(os.path.join(BASE_DIR, '../log', 'debug.log')),
            'formatter': 'verbose'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'WARN'
        },
        '': {
            'formatter': 'verbose',
            'handlers': ['console', 'file'],
            'level': 'INFO'
        }
    },
}


# rest_framework
#
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
    'PAGE_SIZE': 10
}