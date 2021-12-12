#!/bin/sh

apt update -y
apt install -y gettext
python manage.py compilemessages
python manage.py migrate --database default
python manage.py migrate --database mongodb
python manage.py collectstatic --noinput
python manage.py compress
gunicorn livevil_blog.wsgi:application -w 3 -k gthread -b 0.0.0.0:8000 --chdir=/apps
# daphne -b 0.0.0.0 -p 8000 livevil_blog.asgi:application
