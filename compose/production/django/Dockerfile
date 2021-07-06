FROM python:3.9-buster as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./pyproject.toml ./
RUN pip3 install poetry
RUN  ~/.poetry/bin/poetry export -f requirements.txt --output requirements.txt --without-hashes

RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt

FROM python:3.9-buster

ENV APP_HOME=/apps
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .

RUN pip install --no-cache --no-deps /wheels/*

COPY . $APP_HOME

RUN chown -R app:app $APP_HOME

COPY ./compose/production/django/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh