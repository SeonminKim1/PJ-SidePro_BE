FROM python:3.8.0-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /sidepro_be/

WORKDIR /sidepro_be

RUN apt-get update
RUN apt-get -y install cron

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN service cron start

COPY . /sidepro_be/