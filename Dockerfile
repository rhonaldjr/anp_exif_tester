FROM python:latest
LABEL maintainer="Art and Pics Corp."

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN ln -s /usr/bin/pip3 /usr/bin/pip

RUN apt-get update && apt-get install -y gcc libjpeg-dev libc-dev musl-dev zlib1g zlib1g-dev apt-utils

RUN pip install -r ./requirements.txt

#copy the app files and proceed

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static