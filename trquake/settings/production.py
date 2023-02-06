from .base import *
import environ

env = environ.Env()

DEBUG = False
ALLOWED_HOSTS = ["afetharita.com", "api.afetharita.com"]
CORS_ALLOWED_ORIGINS = ["https://afetharita.com"]


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
