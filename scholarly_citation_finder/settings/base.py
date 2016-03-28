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
LANGUAGE_CODE = 'en-us'
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
    'rest_framework',
    'djcelery',
    'django_extensions', # used for debug only
)
PROJECT_APPS = (
    'scholarly_citation_finder.apps.citation',
    'scholarly_citation_finder.apps.citation.mag', # required for celery
    'scholarly_citation_finder.apps.core',
    'scholarly_citation_finder.apps.rest',
    'scholarly_citation_finder.apps.parser',
    'scholarly_citation_finder.apps.tasks',
    'scholarly_citation_finder.lib',
    'scholarly_citation_finder.tools.crawler',
    'scholarly_citation_finder.tools.extractor',
    'scholarly_citation_finder.tools.harvester',
    'scholarly_citation_finder.tools.nameparser',
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
# Database settings
###############################################################################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DEFAULT_DATABASE_NAME', 'scf'),
        'USER': os.getenv('DEFAULT_DATABASE_USER', 'postgres'),
        'PASSWORD': os.getenv('DEFAULT_DATABASE_PASSWORD', 'root'),
        'HOST': '127.0.0.1',
        'PORT': '5432'
    },
    'dblp': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DBLP_DATABASE_NAME', 'dblp'),
        'USER': os.getenv('DBLP_DATABASE_USER', 'dblp'),
        'PASSWORD': os.getenv('DEFAULT_DATABASE_PASSWORD', 'root'),
        'HOST': '127.0.0.1',
        'PORT': '5432'
    },
    'citeseerx': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('CITESEERX_DATABASE_NAME', 'citeseerx'),
        'USER': os.getenv('CITESEERX_DATABASE_USER', 'postgres'),
        'PASSWORD': os.getenv('CITESEERX_DATABASE_PASSWORD', 'root'),
        'HOST': '127.0.0.1',
        'PORT': '5432'
    },
    'mag': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('MAG_DATABASE_NAME', 'mag'),
        'USER': os.getenv('MAG_DATABASE_USER', 'postgres'),
        'PASSWORD': os.getenv('MAG_DATABASE_PASSWORD', 'root'),
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}


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
#CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend'
