FROM python:3.8-slim-buster

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

<<<<<<< HEAD:docker/production/Dockerfile
RUN apt-get update && apt-get upgrade -y
RUN apt-get install git -y

=======
RUN apt-get update && apt-get upgrade -y && apt-get install tini -y
>>>>>>> 35f492edbf9df2524ddbc4bace7cde434a3b4864:.docker/api/Dockerfile
RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY . .

COPY .docker/api/start-django.sh /start-django
RUN chmod +x /start-django

ENTRYPOINT ["/usr/bin/tini", "--", "/bin/bash", "/start-django"]
