"""Base settings
"""
import socket

import environ


APPS_DIR = environ.Path(__file__) - 3

env = environ.Env()

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)

if READ_DOT_ENV_FILE:
    env_file = str(APPS_DIR.path('.env'))
    print('Loading : {}'.format(env_file))
    env.read_env(env_file)
    print('The .env file has been loaded. See base.py for more information')


DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.postgres',
]
THIRD_PARTY_APPS = [
    'corsheaders',
    'rest_framework',
    'django_filters',
    'django_extensions',
]
LOCAL_APPS = [
    'apps.rates.apps.RatesConfig',
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

DEBUG = env.bool('DJANGO_DEBUG', False)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'HOST': env('POSTGRES_HOST'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'PORT': int(env('POSTGRES_PORT', default=5432)),
        'ATOMIC_REQUESTS': True,
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APPS_DIR.path('shared/templates')),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('en', 'English'),
]


_cors_whitelist = env('DJANGO_CORS_ORIGIN_WHITELIST', default='')
CORS_ORIGIN_ALLOW_ALL = (_cors_whitelist == '*')
if not CORS_ORIGIN_ALLOW_ALL:
    CORS_ORIGIN_WHITELIST = _cors_whitelist.replace(' ', '').split(',')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

STATIC_ROOT = str(APPS_DIR('shared/static'))
STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'COERCE_DECIMAL_TO_STRING': True,
}
