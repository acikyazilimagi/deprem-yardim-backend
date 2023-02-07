#!/usr/bin/env bash

# migrations

python manage.py migrate
python manage.py collectstatic --no-input
python manage.py create_default_user

gunicorn trquake.wsgi -w 25 -b 0.0.0.0:80 --reload --log-level info -t 120
