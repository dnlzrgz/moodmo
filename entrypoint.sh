#!/bin/sh

echo 'Running migrations...'
python manage.py migrate

echo 'Collecting static files...'
python manage.py collectstatic --no-input

echo 'Creating superuser...'
python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL

echo 'Starting application...'
gunicorn moodmo.wsgi:application --bind 0.0.0.0:$PORT --workers 4
