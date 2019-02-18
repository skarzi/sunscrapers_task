"""Production settings
"""
from .base import *

SECRET_KEY = env('DJANGO_SECRET_KEY')

REDIS_LOCATION = env('REDIS_LOCATION', default='redis://127.0.0.1:6379/0')
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': False,
        }
    }
}

