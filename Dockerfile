FROM python:3.8.0-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# RUN apk update
# RUN apk add build-base python3-dev py-pip jpeg-dev zlib-dev

COPY requirements.txt /sidepro_be/

WORKDIR /sidepro_be

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /sidepro_be/