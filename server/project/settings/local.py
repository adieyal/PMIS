"""Development settings and globals."""


from os.path import join, normpath

from base import *


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': normpath(join(DJANGO_ROOT, 'local.db')),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

API_CACHE = 60 * 5
########## END CACHE CONFIGURATION


########## TOOLBAR CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
    'debug_toolbar',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}
########## END TOOLBAR CONFIGURATION


LOGGING["loggers"]["apps.projects.management.commands.parsers._projectsheetparser"]["level"] = "WARN"
LOGGING["loggers"]["apps.projects.management.commands.parsers._planningprojectsheetparser"]["level"] = "WARN"
LOGGING["loggers"]["apps.projects.management.commands.parsers._retentionprojectsheetparser"]["level"] = "WARN"

# Used for URL generation in the seeding of ElasticSearch,
# useful anywhere
BASE_URL = 'http://www.backend.dev'

# So we can have separate environments for testing, development
REDIS = {
    # 'host': '127.0.0.1',
    # 'port': 6379,
    'db': 0,
    'unix_socket_path': '/var/run/redis/redis.sock',
}
