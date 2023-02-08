# Afet Harita Backend

The backend project for https://afetharita.com is accessible at https://api.afetharita.com.

Other projects: https://github.com/acikkaynak/deprem-yardim-projesi

## Technologies Used

Python (Django), Postgres (PostgreSQL), Redis, AWS (Elastic Load Balancer, ECS, AWS Fargate), OpenAI (Image to text conversion)

# Running the project

## Dependencies:

[Docker](https://www.docker.com) (opsiyonel): Not necessary for development but makes it easier to install requirements and develop the project. The project runs on AWS ECS in live on Docker.

[PostgreSql](https://www.postgresql.org): Used as the database. Can be directly downloaded from the website or the  [docker image](https://hub.docker.com/_/postgres) can be used.

[Redis](https://redis.io): Used as a queue and cache for asynchronous Celery tasks. Can be directly downloaded (for Linux) or the [docker image](https://hub.docker.com/_/redis) can be used. Running on Docker with WSL is the best option for Windows as the latest version does not work directly.

## Setting up the development environment

After installing Docker, all project can be run with Docker Compose with:

```sh
docker-compose up -d
```

To run only postgres and redis for development:

```sh
docker-compose up -d postgres redis
```

## Python

Python dependency management is provided with poetry.

```
pip install poetry
poetry install
```

to install the required packages. Poetry will create its own environment and install packages there.

Then set the environment variables. Copy the .env.template file to .env and make the necessary settings. With example settings from Compose, it will look like this:

```sh
DJANGO_SECRET_KEY= # secret-key for django
POSTGRES_PASSWORD=debug
POSTGRES_USER=debug
POSTGRES_DB=debug
POSTGRES_HOST=trquake-database
POSTGRES_PORT=5432
CELERY_BROKER_URL=trquake-redis
ZEKAI_USERNAME= # zekai.io username
ZEKAI_PASSWORD= # zekai.io password
DEFAULT_ADMIN_PASSWORD= # password for the first created admin user
```

To create the Django secret key:

```sh
python
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```

To run the project in development mode:

```sh
django-admin createsuperuser
django-admin migrate
django-admin runserver
```

To run the Celery tasks developed for the project:

```sh
celery -A trquake.celery.app worker -B -l DEBUG
```
