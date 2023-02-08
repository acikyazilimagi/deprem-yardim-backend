# Third Party
import environ

# Local Folder
from .base import *

env = environ.Env()

DEBUG = False
ALLOWED_HOSTS = [
    "api.afetharita.com",
    "afetharita.com",
    "backend-alb-708465138.eu-central-1.elb.amazonaws.com",
    "d-back-lb-1711558828.eu-central-1.elb.amazonaws.com",
]
# CORS_ALLOWED_ORIGINS = ["https://afetharita.com", "https://api.afetharita.com", "http://api.afetharita.com"]
CORS_ORIGIN_ALLOW_ALL = True

CSRF_TRUSTED_ORIGINS = ["https://*.afetharita.com", "http://*.afetharita.com", "https://afetharita.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": "5432",
        "ATOMIC_REQUESTS": True,
    }
}
