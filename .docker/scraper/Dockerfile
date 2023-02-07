FROM python:3.8-slim-buster

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install git tini build-essential -y

RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY . .

COPY .docker/scraper/start-django.sh /start-django
RUN chmod +x /start-django

ENTRYPOINT ["/usr/bin/tini", "--", "/bin/bash", "/start-django"]
