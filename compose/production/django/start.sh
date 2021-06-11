#!/bin/sh

poetry run python manage.py migrate --database default
poetry run python manage.py migrate --database mongodb
poetry run python manage.py collectstatic --noinput
poetry run python manage.py compress
poetry run gunicorn livevil_blog.wsgi:application -w 3 -k gthread -b 0.0.0.0:8000 --chdir=/apps
# daphne -b 0.0.0.0 -p 8000 livevil_blog.asgi:application