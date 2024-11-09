FROM python:3.10

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install poetry
COPY . /usr/src/app/

RUN poetry update

