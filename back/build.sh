#!/usr/bin/env bash
# exit on error
set -o errexit

# Установка зависимостей
pip install -r requirements.txt

# Создание и применение миграций
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Создание суперюзера (админа)
python manage.py init_admin

# Сбор статических файлов
python manage.py collectstatic --noinput
