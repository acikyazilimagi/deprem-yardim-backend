# Afet Harita Backend
[ENGLISH VERSION](README.en.md)

https://afetharita.com için back-end projesi. https://api.afetharita.com adresinden erişilebilir.

Diğer projeler: https://github.com/acikkaynak/deprem-yardim-projesi

## Kullanılan teknolojiler

Python (Django), Postgres (PostgreSQL), Redis, AWS (Elastic Load Balancer, ECS, AWS Fargate), OpenAI (Görsellerin metine çevirilmesi)

# Projeyi çalıştırmak

## Bağımlılıklar:

[Docker](https://www.docker.com) (opsiyonel): Geliştirmek için şart değilse de gereksinimleri yüklemeyi ve geliştirme yapmayı kolaylaştıracaktır. Canlıda proje docker üzerinde AWS ECS'lerde çalışmaktadır.

[PostgreSql](https://www.postgresql.org): Veritabanı olarak kullanılmaktadır. Adresten doğrudan bilgisayarınıza indirebilir ya da [docker imajını](https://hub.docker.com/_/postgres) kullanabilirsiniz.

[Redis](https://redis.io): Asenkron Celery görevleri için kuyruk ve cache olarak kullanılmaktadır. Doğrudan bilgisayarınıza indirebilir (Linux için) ya da [docker imajını](https://hub.docker.com/_/redis) kullanabilirsiniz. Windows'ta son versiyon doğrudan çalışmadığı için WSL ile docker'da çalıştırmak en iyi seçenek.

## Geliştirme ortamının hazırlanması

Docker yükledikten sonra tüm projeyi docker-compose ile çalıştırmak için

```sh
docker-compose up -d
```

Geliştirme için sadece postgres ve redisi ayağa kaldırmak için:

```sh
docker-compose up -d postgres redis
```

## Python

Python bağımlılık yönetimi [poetry](https://python-poetry.org/) ile sağlanmaktadır.

```
pip install poetry
poetry install
```

ile gerekli paketleri yükleyebilirsiniz. Poetry kendi ortamını oluşturup paketleri oraya yükleyecektir.

&nbsp;

**Django Secret ile key oluşturmak için:**
```sh
python
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```

Daha sonra ortam değişkenlerini ayarlayın. **.env.template** dosyasını **.env** adıyla kopyalayıp gerekli ayarları yapın.

&nbsp;

Compose'dan gelen örnek ayarlarla aşağıdaki gibi olacaktır:
```sh
DJANGO_SECRET_KEY= # oluşturduğumuz secret key
POSTGRES_PASSWORD=debug
POSTGRES_USER=debug
POSTGRES_DB=debug
POSTGRES_HOST=trquake-database
POSTGRES_PORT=5432
CELERY_BROKER_URL=redis://trquake-redis:6379
ZEKAI_USERNAME= # zekai.co kullanıcı adı
ZEKAI_PASSWORD= # zekai.co şifre
DEFAULT_ADMIN_PASSWORD= # ilk oluşturulan admin kullanıcısı için şifre
```

&nbsp;

**Projeyi development modunda çalıştırmak için:**

```sh
DJANGO_SETTINGS_MODULE=trquake.settings.development django-admin migrate
DJANGO_SETTINGS_MODULE=trquake.settings.development django-admin createsuperuser
DJANGO_SETTINGS_MODULE=trquake.settings.development django-admin collectstatic --no-input
DJANGO_SETTINGS_MODULE=trquake.settings.development django-admin runserver
```
Yukarıdaki komutlar sonucunda çalışan yerel uygulamamızın bilgileri şöyle olacaktır;

Ana Url: http://127.0.0.1:8000/

Admin Url: http://127.0.0.1:8000/admin/

Admin Kullanıcı Adı: ```depremyardim```

Admin Kullanıcı Şifresi: **.env** dosyasında ```DEFAULT_ADMIN_PASSWORD``` kısmında tanımladığınız şifre.

&nbsp;

**Celery tasklarını çalıştırmak için:**

```sh
celery -A trquake.celery.app worker -B -l DEBUG
```