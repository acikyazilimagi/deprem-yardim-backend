#!/usr/bin/env bash

# migrations
python manage.py makemigrations
python manage.py migrate

gunicorn trquake.wsgi -w 25 -b 0.0.0.0:80 --reload --log-level debug -t 120
