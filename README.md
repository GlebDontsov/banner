# Сервис баннеров

## Описание задачи
Возвращает пользователю баннер по фиче и тегу, в зависимости от прав,
предусмотрено кеширование

## Stack

>Language: __Python 3__<br>
Web framework: __FastAPI__<br>
Database: __PostgreSQL__, __Redis__<br>

Другое: Docker, SQLAlchemy, pytest

## Информация о доступе к документации
> - <p>docs/v.1.0.0/api.html — Документация;<br>

## Локальный запуск сервиса
 1. Установка зависимостей, использовать poetry version 1.1.12 или выше
```
poetry shell
```
```
poetry install
```
2. Заполнить .env файл, пример смотреть в .env_example
3. Сделать миграции в созданную БД
```
export PYTHONPATH=$(pwd)/src
```
```
alembic -c src/alembic.ini upgrade a359a29e7732
```
4. Запуск сервиса
```
 python src/app/service.py
```
5. Документацию можно открыть в docs/v.1.0.0/api.html и отправлять от туда запросы.
Чтобы получить токен юзера использовать username = user, password = 123123, а админа - 
username = admin, password = 123456, данные можно установить свои, но тогда не забудьте
 сгенирировать хеш пароля.
6. Запуск линтер
```
 flake8 src/app
```
```
 mypy src/app
```
7. Запуск тестов
```
 pytest src/tests
```

## Инструкции для развертывания сервиса в Docker
1. Сборка образов и запуск сервиса, перед этим заполнить .env, как .env_example
```
 docker compose up
```
2. Войти в контейнер
```
 docker exec -it <container_id> bash
```
3. Запуск тестов в контейнере
```
PYTHONPATH="$(pwd)/src" pytest src/tests
```
4. Запуск линтера в контейнере
```
 flake8 src/app
```
```
 mypy src/app
```
