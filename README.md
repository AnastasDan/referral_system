![Python](https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/Django-%23092E20.svg?style=flat&logo=django&logoColor=white)
![Django Rest Framework](https://img.shields.io/badge/Django%20Rest%20Framework-ff1709?style=flat&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)

# Мини-проект «Реферальная система»

Простой RESTful API сервис для реферальной системы.

## Как запустить проект

1. Клонируем себе репозиторий:

```bash 
git clone git@github.com:AnastasDan/referral_system.git
```
2. Переходим в директорию referral_system/, создаем файл .env и заполняем его. Список данных указан в файле .env.example.

3. Запускаем проект:

```bash
docker compose -f docker-compose.yml up
```

4. После запуска выполняем миграции, сбор статических файлов, а также выгрузку ингредиентов в базу данных. По желанию можно создать суперпользователя:

```bash
docker compose -f docker-compose.yml exec backend python manage.py migrate

docker compose -f docker-compose.yml exec backend python manage.py createsuperuser
```

5. Проект будет доступен по данной ссылке - <http://localhost:9000/api/> а документация к API - <http://localhost:9000/redoc/> или <http://localhost:9000/swagger/>
