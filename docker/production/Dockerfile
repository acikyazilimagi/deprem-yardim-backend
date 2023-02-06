FROM python:3.8-slim-buster

# define environments
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV DJANGO_SETTINGS_MODULE=trquake.settings.production

WORKDIR /app

RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY docker/development/start-django.sh /start-django
RUN chmod +x /start-django

COPY ./ ./

CMD ["/start-django"]
