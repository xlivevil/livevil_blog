FROM centos:7.5.1804

RUN yum -y update && yum -y install openssl-devel bzip2-devel zlib zlib-devel expat-devel gdbm-devel readline-devel sqlite-devel wget MySQL-python mysql-devel gcc gcc-devel python3-devel automake autoconf libtool make libffi-devel
RUN wget https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz
RUN tar zxvf Python-3.7.7.tgz -C /usr/local
WORKDIR /usr/local/Python-3.7.7/
RUN ./configure LD_RUN_PATH=/usr/local/lib LDFLAGS="-L/usr/local/lib" CPPFLAGS="-I/usr/local/include" && make LD_RUN_PATH=/usr/local/lib && make install

ENV PYTHONUNBUFFERED 1

WORKDIR /apps

RUN pip3 install 'django==2.2' markdown gunicorn django-pure-pagination 'elasticsearch>=5,<6' 'django-haystack==3.0.0b2' django-allauth requests pillow django-debug-toolbar djangorestframework django-crispy-forms django-reversion django-pure-pagination mysqlclient django-redis django-filter supervisor

COPY . /apps
COPY ./compose/production/django/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh

