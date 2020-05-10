#!/bin/sh

python3 manage.py migrate
python3 manage.py collectstatic --noinput
gunicorn livevil_blog.wsgi:application -w 4 -k gthread -b 0.0.0.0:8000 --chdir=/apps
