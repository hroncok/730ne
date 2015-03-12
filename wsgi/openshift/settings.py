"""
Django settings for openshift project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import imp

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

ON_OPENSHIFT = False
if 'OPENSHIFT_REPO_DIR' in os.environ:
    ON_OPENSHIFT = True
    AUTH_FILE = os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'auth.conf')
else:
    AUTH_FILE = os.path.join(BASE_DIR, 'auth.conf')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
default_keys = {'SECRET_KEY': 'tjy&7h%c=q01+c5i@_-t)&n2c+y*tn7v_)vbdksnlv@s5qh%e_'}
use_keys = default_keys
if ON_OPENSHIFT:
    imp.find_module('openshiftlibs')
    import openshiftlibs
    use_keys = openshiftlibs.openshift_secure(default_keys)

SECRET_KEY = use_keys['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
if ON_OPENSHIFT:
    DEBUG = False
else:
    DEBUG = True

TEMPLATE_DEBUG = DEBUG

if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = ['*']

ADMINS = (
    ('Miro Hroncok', 'miro@hroncok.cz'),
)
MANAGERS = ADMINS

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'signatures',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# If you want configure the REDISCLOUD
if 'REDISCLOUD_URL' in os.environ \
   and 'REDISCLOUD_PORT' in os.environ and 'REDISCLOUD_PASSWORD' in os.environ:
    redis_server = os.environ['REDISCLOUD_URL']
    redis_port = os.environ['REDISCLOUD_PORT']
    redis_password = os.environ['REDISCLOUD_PASSWORD']
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '%s:%d' % (redis_server, int(redis_port)),
            'OPTIONS': {
                'DB': 0,
                'PARSER_CLASS': 'redis.connection.HiredisParser',
                'PASSWORD': redis_password,
            }
        }
    }
    MIDDLEWARE_CLASSES = ('django.middleware.cache.UpdateCacheMiddleware',) + \
        MIDDLEWARE_CLASSES + \
        ('django.middleware.cache.FetchFromCacheMiddleware',)


ROOT_URLCONF = 'urls'

if ON_OPENSHIFT:
    WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if ON_OPENSHIFT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['OPENSHIFT_APP_NAME'],
            'USER': os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],
            'PASSWORD': os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],
            'HOST': os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
            'PORT': os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Social auth
AUTHENTICATION_BACKENDS = (
    'fitauth.FITOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/'

try:
    with open(AUTH_FILE) as f:
        auth = f.readlines()
    SOCIAL_AUTH_FIT_KEY = auth[0].rstrip()
    SOCIAL_AUTH_FIT_SECRET = auth[1].rstrip()
except Exception:
    pass

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',  # <--- enable this one
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'cs-cz'

TIME_ZONE = 'Europe/Prague'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
STATIC_URL = '/static/'
