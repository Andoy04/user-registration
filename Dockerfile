FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir /user_registration_api

WORKDIR /user_registration_api

COPY . .
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt


RUN adduser -D andoy
USER andoy