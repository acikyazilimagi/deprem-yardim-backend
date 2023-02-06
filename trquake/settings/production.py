from .base import *
import environ

env = environ.Env()

DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ALLOWED_ORIGINS = ["https://afetharita.com", "https://api.afetharita.com"]


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
