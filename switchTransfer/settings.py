"""
Django settings for switchTransfer project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_)&=bnlyoggtvs-f3$mr^nq(hk5fl-8j^(nq)-7_(iv4-uk=yl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
SHARED_APPS = (
    'tenant_schemas',  # mandatory, should always be before any django app
    'switch', # you must list the app where your tenant model resides in

    'django.contrib.contenttypes',

    # everything below here is optional
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
)

TENANT_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'myswitch',
    'accounts',

    # your tenant-specific apps
    #'myapp.hotels',
    #'myapp.houses',
)

TENANT_MODEL = "switch.Client" # app.Model
#TENANT_DOMAIN_MODEL = 'switch.Domain'

MEDIA_ROOT = '/data/media'
MEDIA_URL ='/media/'
DEFAULT_FILE_STORAGE = 'tenant_schemas.storage.TenantFileSystemStorage'


# Application definition

INSTALLED_APPS = [
    'tenant_schemas',
    'switch.apps.SwitchConfig',
    'myswitch',
    'accounts',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'tenant_schemas.middleware.TenantMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

PUBLIC_SCHEMA_URLCONF = 'switchTransfer.public_urls'
ROOT_URLCONF = 'switchTransfer.urls'

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

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    #...
)

WSGI_APPLICATION = 'switchTransfer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'tenant_schemas.postgresql_backend',
        'NAME':'#',
        'USER':'#',
        'PASSWORD':'#',
        'HOST':'#',
        'PORT':'5432',
    }
}

DATABASE_ROUTERS = (
    'tenant_schemas.routers.TenantSyncRouter',
)
'''
LOGGING = {
    'filters': {
        'tenant_context': {
            '()': 'tenant_schemas.log.TenantContextFilter'
        },
    },
    'formatters': {
        'tenant_context': {
            'format': '[%(schema_name)s:%(domain_url)s] '
            '%(levelname)-7s %(asctime)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'filters': ['tenant_context'],
        },
    },
}'''

TENANT_LIMIT_SET_CALLS = True


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
PROJECT_ROOT   =   os.path.join(os.path.abspath(__file__))
STATIC_ROOT  =   os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra lookup directories for collectstatic to find static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

#  Add configuration for static files storage using whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# redirect user once login
LOGIN_REDIRECT_URL = '/dashboard'
LOGOUT_REDIRECT_URL = '/accounts/login'
