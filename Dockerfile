FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev libpng-dev jpeg-dev jpeg zlib-dev && \
    apk add postgresql-dev bash

RUN apk add --virtual python-imaging

RUN mkdir /config
ADD /config/requirements.txt /config/
RUN pip install --upgrade pip
RUN pip install -r /config/requirements.txt
RUN mkdir /src
WORKDIR /src
