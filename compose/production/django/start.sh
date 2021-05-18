#!/bin/sh

python3 manage.py migrate
python3 manage.py collectstatic --noinput
python3 manage.py compress
gunicorn livevil_blog.wsgi:application -w 4 -k gthread -b 0.0.0.0:8000 --chdir=/apps
# daphne -b 0.0.0.0 -p 8000 livevil_blog.asgi:application