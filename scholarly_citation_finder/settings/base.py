"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os

###############################################################################
# Basic settings
###############################################################################

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_URLCONF = 'scholarly_citation_finder.urls'
WSGI_APPLICATION = 'scholarly_citation_finder.wsgi.application'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'e5zjfb$nbtq(u(go5q9etj^t@mhl2kr&w_np%3_zq+g4rx1n!l')

# Internationalization
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False


###############################################################################
# Applications and middleware classes
###############################################################################

# Application definition
PREREQ_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'djcelery',
)
PROJECT_APPS = (
    'scholarly_citation_finder.api.citation',
    'scholarly_citation_finder.api.crawler',
    'scholarly_citation_finder.api.extractor',
    'scholarly_citation_finder.api.harvester',
    'scholarly_citation_finder.apps.core',
    'scholarly_citation_finder.apps.frontend',
    'scholarly_citation_finder.apps.rest',
    'scholarly_citation_finder.lib',
)
INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.security.SecurityMiddleware'
)


###############################################################################
# Templates and static files
###############################################################################

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.getenv('STATIC_ROOT', os.path.join(BASE_DIR, 'static'))
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '../public'),
]


###############################################################################
# Celery
###############################################################################

# Celery settings
BROKER_URL = os.getenv('BROKER_URL', 'amqp://guest:guest@localhost//')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'djcelery.backends.database:DatabaseBackend')
