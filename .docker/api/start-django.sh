#!/usr/bin/env bash

# migrations
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input

gunicorn trquake.wsgi -w 25 -b 0.0.0.0:80 --reload --log-level debug -t 120
