#!/usr/bin/env bash
# start.sh

set -o errexit

python manage.py migrate

gunicorn your_project_name.wsgi:application --bind 0.0.0.0:$PORT
