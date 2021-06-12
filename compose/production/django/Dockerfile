FROM centos:7.5.1804

RUN yum -y update && yum -y install openssl-devel bzip2-devel zlib zlib-devel expat-devel gdbm-devel \
    && yum -y install readline-devel sqlite-devel wget MySQL-python mysql-devel gcc gcc-devel \
    && yum -y install python3-devel automake autoconf libtool make libffi-devel gettext
RUN wget https://www.python.org/ftp/python/3.9.4/Python-3.9.4.tgz \
    && tar zxvf Python-3.9.4.tgz -C /usr/local
WORKDIR /usr/local/Python-3.9.4/
RUN ./configure LD_RUN_PATH=/usr/local/lib LDFLAGS="-L/usr/local/lib" CPPFLAGS="-I/usr/local/include" && make LD_RUN_PATH=/usr/local/lib && make install

ENV PYTHONUNBUFFERED 1

WORKDIR /apps

# RUN pip3 install 'django==3.2' markdown gunicorn django-pure-pagination 'elasticsearch>=5,<6' 'django-haystack==3.0' django-allauth requests pillow django-debug-toolbar djangorestframework django-crispy-forms django-reversion django-pure-pagination mysqlclient django-redis django-filter supervisor
# RUN pip3 install django-contrib-comments django-mptt drf-yasg
# RUN pip3 install django_compressor beautifulsoup4 html5lib slimit calmjs.parse csscompressor brotli django-grappelli subdomains
# RUN STATIC_DEPS=true pip3 install lxml
RUN pip3 install poetry

COPY . /apps
COPY ./compose/production/django/start.sh /start.sh
RUN poetry run pip3 install rcssmin --install-option="--without-c-extensions"
RUN poetry install --no-dev
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh

# FROM python:3.9-alpine as builder

# WORKDIR /usr/src/app

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # add curl for poetry
# RUN apk update && apk add gcc python3-dev musl-dev curl  mariadb-dev

# COPY ./pyproject.toml ./

# RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# RUN  ~/.poetry/bin/poetry export -f requirements.txt --output requirements.txt --without-hashes

# RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt


# # === FINAL IMAGE ===

# FROM python:3.9-alpine

# RUN addgroup -S app && adduser -S app -G app

# # Create directories app_home and static directories
# ENV HOME=/home/app
# ENV APP_HOME=/home/app/web
# RUN mkdir $APP_HOME
# WORKDIR $APP_HOME

# # Copy dependencies from builder image
# RUN apk update && apk add --no-cache libpq mariadb-connector-c-dev

# COPY --from=builder /usr/src/app/wheels /wheels
# COPY --from=builder /usr/src/app/requirements.txt .

# RUN pip install --no-cache --no-deps /wheels/*

# COPY . $APP_HOME

# RUN chown -R app:app $APP_HOME

# USER app

# RUN python manage.py collectstatic --noinput

# CMD sleep 15 && gunicorn microservice.wsgi:application --bind 0.0.0.0:8000
