import dj_database_url
from ShipSecure.settings.base import *

ALLOWED_HOSTS = ['ship-secure.herokuapp.com']

DEBUG = True

DATABASES = {"default": dj_database_url.config(conn_max_age=600, ssl_require=True)}
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
   }
}