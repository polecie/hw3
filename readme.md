<div align="center">

![pre-commit](https://github.com/polecie/hw3/actions/workflows/pre-commit.yaml/badge.svg)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)](https://github.com/pre-commit/pre-commit)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Flake8](https://img.shields.io/badge/flake8-checked-yellow.svg?style=flat)](https://flake8.pycqa.org/en/latest/)
[![Code syntax: pyupgrade](https://img.shields.io/badge/pyupgrade-checked-orange.svg)](https://github.com/psf/black)
[![Autopep8](https://img.shields.io/badge/autopep8-checked-red.svg?style=flat)](https://github.com/pre-commit/mirrors-autopep8)

</div>

## Технологии

*Основные*

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/Rabbitmq-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
![Celery](https://img.shields.io/badge/celery-88CE02?style=for-the-badge&logo=celery&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

*Дополнительно*

![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)

## Запуск приложения

Клонировать репозиторий [`https://github.com/polecie/hw3`](https://github.com/polecie/hw3)

### Запуск контейнера с приложением

*При необходимости можно заменить переменные окружения из файла `.env` на свои*

Для запуска основного приложения необходимо использовать команды `make up`

Для остановки рекомендуется использовать `make down` для избежания конфликтов с портами

**После запуска приложения**

*Документация openapi доступна по адресу* [`http://0.0.0.0:8000/api/openapi`](http://0.0.0.0:8000/api/openapi)

*Админка rabbitmq доступна тут* [`http://0.0.0.0:15672/`](http://0.0.0.0:15672/)

*Мониторинг задач через* `flower` *доступен на* [`http://localhost:5555/`](http://localhost:5555/)

**NOTA BENE**: основной кеш находится в `0` базе данных редиса, кеш для ручек с отчетом в `1`, кеш для тестов во `2`

### Запуск контейнера с тестами

Для запуска тестов необходимо использовать команды `make test`

## Описание

### Задачи

1. Требуется написать REST API по работе с меню ресторана, необходимо реализовать все CRUD операции
2. Написать тесты для разработанных ендпоинтов API
3. Обернуть программные компоненты в контейнеры
4. Добавить `pre-commit` хуки
5. Описать ендпоинты API в соответствии с openapi
6. Кешировать `GET` запросы
7. Разделить бизнес логику и запросы в базу данных
8. Приложение должно быть асинхронным
9. Добавить в проект фоновую задачу по генерации меню ресторана в виде excel-документа
10. Добавить +2 ендпоинта для запуска фоновой задачи и получения результата в виде ссылки на файл, `POST` и `GET` соответственно
11. Добавить отдельный `GET` ендпоинт, который заполнит базу данных тестовыми данными для последующей генераций меню в excel-файл

### Требования
1. Данные меню, подменю, блюд для генераций excel-файла, должны доставаться одним ORM-запросом в БД (использовать подзапросы и агрегирующие функций SQL)
2. Код должен проходить все линтеры `(black, autopep, flake8, mypy, isort)`
3. Проект должен запускаться по одной команде, а тесты по другой
4. Проект должен проходить все `Postman` тесты
5. Тесты написанные самостоятельно, должны быть актуальны, запускаться и успешно проходить
6. Код должен соответствовать принципам `SOLID, DRY, KISS`

### Условия
Даны 3 сущности: **Меню, Подменю, Блюдо**
- Блюдо не может быть привязано напрямую к меню, минуя подменю
- Блюдо не может находиться в 2-х подменю одновременно
- Подменю не может находиться в 2-х меню одновременно
- Если удалить меню, должны удалиться все подменю и блюда этого меню
- Если удалить подменю, должны удалиться все блюда этого подменю
- Цены блюд выводить с округлением до 2 знаков после запятой
- Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд в этом меню
- Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю

### Зависимости
* У меню есть подменю, которые к нему привязаны
* У подменю есть блюда

## Реализация

*Схема ендпоинтов для меню, подменю и блюда*

![endpoints_menu_submenu_dish](https://user-images.githubusercontent.com/68993459/216778866-eeb9a507-2768-4d21-89ae-2d4670283d47.png)

*Схема ендпоинтов для отчета и генерации тестовых данных*

![endpoints_report](https://user-images.githubusercontent.com/68993459/216778946-86d1fc67-d539-40eb-b6ab-d9d9c2849fca.png)

*Примеры статусов ответов*
