![alt text](https://acik-kaynak.org/_next/static/media/logo.19284790.svg)

[![Afet-Harita](https://img.shields.io/badge/Afet-Harita-blue)](https://www.afetharita.com.com) [![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg?logo=python&labelColor=yellow)](https://www.python.org) [![Docker](https://img.shields.io/badge/docker-build-important.svg?logo=Docker)](https://www.docker.com) [![Platform](https://img.shields.io/badge/platform-windows%2Flinux-green.svg)](https://gl.bg-tek.net/shaman/pentestbx-ets-module) [![Django](https://img.shields.io/badge/django%20version-4.1.6-blue)](https://www.djangoproject.com) [![DjangoRest](https://img.shields.io/badge/django%20rest-3.14.0-blue)](https://www.djangoproject.com) [![nginx](https://img.shields.io/badge/NGINX-blue)](https://www.nginx.com) [![git](https://badgen.net/badge/redis/7.0.3+/red?icon=redis)](https://redis.com/)
[![celery](https://badgen.net/badge/celery/5.2.6+/red?icon=celery)](https://docs.celeryq.dev/) [![aws](https://badgen.net/badge/AWS/services//red?icon=redis)](https://aws.amazon.com/) 


# Afet Harita Backend
[ENGLISH VERSION](README.en.md)

https://afetharita.com için back-end projesi. https://api.afetharita.com adresinden erişilebilir.

Diğer projeler: https://github.com/acikkaynak/deprem-yardim-projesi

## Mimari
![image](docs/afetharita-backend.png)

## Kullanılan teknolojiler

Python (Django), Postgres (PostgreSQL), Redis, AWS (Elastic Load Balancer, ECS, AWS Fargate), OpenAI (Görsellerin metine çevirilmesi)

# Projeyi çalıştırmak

## Bağımlılıklar:

[Docker](https://www.docker.com) (opsiyonel): Geliştirmek için şart değilse de gereksinimleri yüklemeyi ve geliştirme yapmayı kolaylaştıracaktır. Canlıda proje docker üzerinde AWS ECS'lerde çalışmaktadır.

[PostgreSql](https://www.postgresql.org): Veritabanı olarak kullanılmaktadır. Adresten doğrudan bilgisayarınıza indirebilir ya da [docker imajını](https://hub.docker.com/_/postgres) kullanabilirsiniz.

[Redis](https://redis.io): Asenkron Celery görevleri için kuyruk ve cache olarak kullanılmaktadır. Doğrudan bilgisayarınıza indirebilir (Linux için) ya da [docker imajını](https://hub.docker.com/_/redis) kullanabilirsiniz. Windows'ta son versiyon doğrudan çalışmadığı için WSL ile docker'da çalıştırmak en iyi seçenek.

## Geliştirme ortamının hazırlanması

```sh
git clone https://github.com/acikkaynak/deprem-yardim-backend.git
```

Docker yükledikten sonra tüm projeyi docker-compose ile çalıştırmak için

```sh
docker-compose up --build -d
```

Geliştirme için sadece postgres ve redisi ayağa kaldırmak için:

```sh
docker-compose up -d database redis
```

## Python

Python bağımlılık yönetimi poetry ile sağlanmaktadır.

```
pip install poetry
poetry install
```

ile gerekli paketleri yükleyebilirsiniz. Poetry kendi ortamını oluşturup paketleri oraya yükleyecektir.

Daha sonra ortam değişkenlerini ayarlayın. .env.template dosyasını .env adıyla kopyalayıp gerekli ayarları yapın. Compose'dan gelen örnek ayarlarla aşağıdaki gibi olacaktır:

```sh
DJANGO_SECRET_KEY= # django için secret-key
POSTGRES_PASSWORD=debug
POSTGRES_USER=debug
POSTGRES_DB=debug
POSTGRES_HOST=trquake-database
POSTGRES_PORT=5432
CELERY_BROKER_URL=trquake-redis
ZEKAI_USERNAME= # zekai.co kullanıcı adı
ZEKAI_PASSWORD= # zekai.co şifre
DEFAULT_ADMIN_PASSWORD= # ilk oluşturulan admin kullanıcısı için şifre
```

Django Secret key oluşturmak için:

```sh
python
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```

Projeyi development modunda açmak için:

```sh
django-admin migrate
django-admin createsuperuser
django-admin collectstatic --no-input
django-admin runserver
```

Celery için geliştirilen taskları çalıştırmak için:

```sh
celery -A trquake.celery.app worker -B -l DEBUG
```