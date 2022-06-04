import dj_database_url
from ShipSecure.settings.base import *

ALLOWED_HOSTS = ['https://ship-secure.herokuapp.com']

DEBUG = True

DATABASES = {"default": dj_database_url.config(conn_max_age=600, ssl_require=True)}
