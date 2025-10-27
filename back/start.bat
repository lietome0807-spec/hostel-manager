@echo off
echo =======================================
echo  Hostel Manager Backend - Startup
echo =======================================
echo.

:: Проверка виртуального окружения
if not exist "venv\" (
    echo Создание виртуального окружения...
    python -m venv venv
)

:: Активация виртуального окружения
echo Активация виртуального окружения...
call venv\Scripts\activate

:: Установка зависимостей
echo.
echo Установка зависимостей...
pip install -r requirements.txt

:: Миграции
echo.
echo Применение миграций...
python manage.py makemigrations
python manage.py migrate

:: Создание супер-админа
echo.
echo Создание супер-администратора...
python manage.py init_admin

:: Запуск сервера
echo.
echo =======================================
echo  Запуск сервера на http://127.0.0.1:8000
echo =======================================
echo.
python manage.py runserver

pause
