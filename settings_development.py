# -*- coding: utf-8 -*-
import os.path
import sys
import re
import djcelery
djcelery.setup_loader()

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bsg.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
BROKER_URL = 'redis://localhost:6379/0'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Detroit'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'France'),
    ('lt', 'Lithuanian'),
    ('pl', 'Polish'),
    ('ru', 'Russian'),
    ('zh_CN', 'Chinese'),
    ('de', 'German'),
    ('vi', 'Vietnamese'),
    ('it', 'Italian'),
    ('cs', 'Czech'),
    ('ca', 'Catalan'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collected/')
STATIC_URL = '/static/'


STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.

if not hasattr(globals(), 'SECRET_KEY'):
    SECRET_FILE = os.path.join(PROJECT_ROOT, 'secret.txt')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        try:
            from random import choice
            import string
            symbols = ''.join((string.lowercase, string.digits, string.punctuation ))
            SECRET_KEY = ''.join([choice(symbols) for i in range(50)])
            secret = file(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            raise Exception('Please create a %s file with random characters to generate your secret key!' % SECRET_FILE)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',

)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
)

ACCOUNT_ACTIVATION_DAYS = 7

AUTHENTICATION_BACKENDS = (
    'backends.CaseInsensitiveModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',
    'django_nvd3',
    'paypal.standard.ipn',
    'djcelery',
    'djrill',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',
    'events',
    'sponsorship',
    'seatmap',
    'pages',
    'tournaments',
    'schedule',
)

EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'

FORCE_SCRIPT_NAME = ''

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
    'joomla_password_hasher.JoomlaPasswordHasher' 
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Account settings
ACCOUNT_ACTIVATION_DAYS = 10
LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'publish_stream'],
        'METHOD': 'js_sdk'  # instead of 'oauth2'
    }
}
LOGIN_URL = '/accounts/login/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

#Cache settings
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

# All API keys in this configuration should be for development purposes ONLY.

RECAPTCHA_PUBLIC_KEY = '6Lfgv8ESAAAAAOCwstLnTDgClcfGBVoKuc6pypfu'
RECAPTCHA_PRIVATE_KEY = '6Lfgv8ESAAAAAHbUjSt1YGoLQgSnX4VYzEJHIvwT'

PAYPAL_RECEIVER_EMAIL = 'wiede1_1297892766_biz@cmich.edu'
CHALLONGE_USERNAME = 'tomsoverbaghdad'
CHALLONGE_API_KEY = 'aetvcd2xwyprukz8g6jyx38zc4425dxpzdf2dbxr'

MANDRILL_API_KEY = 'HLxHRFlVtBi6Saq2INoWYQ'

STRIPE_SECRET_KEY = 'sk_test_ViTBDqReF6Y3dDmKgVFzomvH' 
STRIPE_PUBLISHABLE_KEY = 'pk_test_oj0oFdaaIkroXMhwqXeJA55C'

SERVER_EMAIL = 'Big Shot Gaming <bigshot@bigshotgaming.com>'
DEFAULT_FROM_EMAIL = 'Big Shot Gaming <bigshot@bigshotgaming.com>'



try:
    from local_settings import *
except ImportError:
    pass
