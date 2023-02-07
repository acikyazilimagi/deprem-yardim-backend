from .base import *
import environ

env = environ.Env()

DEBUG = False
ALLOWED_HOSTS = ["api.afetharita.com", "afetharita.com"]
# CORS_ALLOWED_ORIGINS = ["https://afetharita.com", "https://api.afetharita.com", "http://api.afetharita.com"]
CORS_ORIGIN_ALLOW_ALL = True

CSRF_TRUSTED_ORIGINS = ["https://*.afetharita.com", "http://*.afetharita.com", "https://afetharita.com"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": "5432",
    }
}
