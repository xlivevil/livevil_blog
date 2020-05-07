FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

WORKDIR /apps

RUN pip install pipenv\

COPY Pipfile /apps/Pipfile
COPY Pipfile.lock /apps/Pipfile.lock
RUN pipenv install --system --deploy --ignore-pipfile

COPY ./compose/local/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh