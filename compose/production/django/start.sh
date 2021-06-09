#!/bin/sh

poetry run manage.py migrate
poetry run manage.py collectstatic --noinput
poetry run manage.py compress
poetry run gunicorn livevil_blog.wsgi:application -w 4 -k gthread -b 0.0.0.0:8000 --chdir=/apps
# daphne -b 0.0.0.0 -p 8000 livevil_blog.asgi:application