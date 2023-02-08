# Third Party
from celery import Celery
from celery.schedules import crontab

app = Celery("trquake")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    "collect_tweets": {
        "task": "tweets.tasks.collect_tweets",
        "schedule": 300.0,
    },
    "collect_deprem_address_tweets": {
        "task": "tweets.tasks.collect_deprem_address_tweets",
        "schedule": 300.0,
    },
}
