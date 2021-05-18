FROM centos:7.5.1804

RUN yum -y update && yum -y install openssl-devel bzip2-devel zlib zlib-devel expat-devel gdbm-devel \
    && yum -y install readline-devel sqlite-devel wget MySQL-python mysql-devel gcc gcc-devel
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
# TODO: use poetry to install dependencies
RUN pip3 install poetry && poetry install --no-dev

COPY . /apps
COPY ./compose/production/django/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh
