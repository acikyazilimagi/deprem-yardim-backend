from .base import *
import environ

env = environ.Env()

DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ALLOWED_ORIGINS = ["https://afetharita.com", "https://api.afetharita.com", "http://api.afetharita.com"]
CSRF_TRUSTED_ORIGINS = ["https://*.afetharita.com", "http://*.afetharita.com", "https://afetharita.com"]
print("CSRF_TRUSTED_ORIGINS", CSRF_TRUSTED_ORIGINS)

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
