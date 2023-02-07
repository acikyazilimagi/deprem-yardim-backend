#!/usr/bin/env bash

# migrations

python manage.py migrate
python manage.py collectstatic --no-input
python manage.py create_default_user

python manage.py runserver 0.0.0.0:8000
