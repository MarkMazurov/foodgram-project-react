FROM python:3.7-slim-buster

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

WORKDIR /app

COPY . /app

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

CMD gunicorn foodgram.wsgi:application --bind 0:8000