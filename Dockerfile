FROM python:3.12-alpine

WORKDIR /app

# Установка poetry
RUN pip install poetry --no-cache-dir

# Копирование файлов для установки зависимостей
COPY poetry.lock /app/
COPY pyproject.toml /app/
# Установка зависимостей проекта с помощью Poetry
RUN poetry config virtualenvs.create false && \
poetry install --no-cache


# Копирование файлов проекта
COPY . .



