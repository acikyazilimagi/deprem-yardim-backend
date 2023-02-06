from trquake.celery import app


@app.task
def collect_tweets():
    print("collect tweets")
