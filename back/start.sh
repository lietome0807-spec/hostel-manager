#!/bin/bash

echo "======================================="
echo " Hostel Manager Backend - Startup"
echo "======================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Активация виртуального окружения..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Установка зависимостей..."
pip install -r requirements.txt

# Migrations
echo ""
echo "Применение миграций..."
python manage.py makemigrations
python manage.py migrate

# Create super admin
echo ""
echo "Создание супер-администратора..."
python manage.py init_admin

# Start server
echo ""
echo "======================================="
echo " Запуск сервера на http://127.0.0.1:8000"
echo "======================================="
echo ""
python manage.py runserver
