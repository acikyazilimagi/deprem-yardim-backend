# Standard Library
import socket

# Third Party
import environ

# Local Folder
from .base import *

env = environ.Env()

INSTALLED_APPS += ["debug_toolbar", "django_extensions"]  # noqa: F405

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]

# Shell Plus
SHELL_PLUS_PRINT_SQL = True

CONN_MAX_AGE=600

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": "5432",
    }
}


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": [
            "redis://trquake-cache:6379",
        ],
    }
}
CACHE_MIDDLEWARE_ALIAS = "default"  # which cache alias to use
CACHE_MIDDLEWARE_SECONDS = 600  # number of seconds to cache a page for (TTL)
# should be used if the cache is shared across multiple sites that use the same Django instance
CACHE_MIDDLEWARE_KEY_PREFIX = ""
