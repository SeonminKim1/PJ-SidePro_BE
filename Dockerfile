FROM python:3.8.0-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /sidepro_be

COPY requirements.txt .

RUN apt-get update && apt-get install -y cron

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN service cron start

COPY . .