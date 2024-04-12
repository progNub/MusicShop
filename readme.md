Для успешного запуска проекта достаточно сделать миграции, и запустить файл [testFaker.py](testFaker.py), он заполнит базу тестовыми данными, все запустится на sqlite3.

Для запуска на PostgreSQL нужны переменные окружения:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DATABASE_NAME`
- `DATABASE_USER`
- `DATABASE_PASSWORD`
- `DATABASE_HOST`