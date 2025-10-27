# 🏨 Hostel Manager - Полная система управления хостелом

Современная система управления хостелом с Django REST API бэкендом и красивым фронтендом.

## 🌟 Возможности

### Для Администратора (Логин: `Kvv`, Пароль: `Kvv08072001`):

#### 👥 Управление пользователями:
- ✅ Принятие или отклонение запросов на регистрацию
- ✅ Просмотр логинов пользователей (пароли зашифрованы для безопасности)
- ✅ Просмотр количества пользователей в системе
- ✅ Удаление пользователей
- ✅ Блокировка пользователей
- ✅ Разблокировка пользователей
- ✅ Установка срока использования для каждого пользователя
- ✅ Полный журнал аудита всех действий с IP адресами

#### 🔒 Безопасность:
- ✅ JWT токен авторизация (защита от оффлайн использования)
- ✅ Хэширование паролей (PBKDF2 с солью)
- ✅ CSRF защита
- ✅ XSS защита
- ✅ Разграничение прав доступа
- ✅ Журнал всех действий
- ✅ Защита от брутфорса
- ✅ Secure cookies и sessions

### Для обычных пользователей:
- 📝 Регистрация с последующим одобрением администратора
- 🔐 Безопасная авторизация
- 🏠 Управление комнатами хостела
- 🛏️ Управление кроватями (одиночные и двухъярусные)
- 👤 Управление жильцами
- 💰 Учёт платежей
- 📊 Статистика занятости
- 🌍 Многоязычность (Русский, Узбекский, English)
- 📱 Адаптивный дизайн

## 📁 Структура проекта

```
HostelManager/
├── back/                          # Django бэкенд
│   ├── hostel_project/           # Настройки проекта
│   │   ├── settings.py          # Конфигурация
│   │   ├── urls.py              # Главные URL
│   │   └── wsgi.py              # WSGI конфигурация
│   ├── hostel_app/              # Основное приложение
│   │   ├── models.py            # Модели БД
│   │   ├── views.py             # API Views
│   │   ├── serializers.py       # DRF Сериализаторы
│   │   ├── urls.py              # URL маршруты
│   │   ├── admin.py             # Django Admin
│   │   └── management/          # Команды управления
│   │       └── commands/
│   │           └── init_admin.py # Создание супер-админа
│   ├── manage.py                # Django CLI
│   ├── requirements.txt         # Python зависимости
│   ├── start.bat               # Скрипт запуска (Windows)
│   └── README.md               # Документация бэкенда
│
├── front/                        # Фронтенд
│   ├── index.html              # Главное приложение
│   ├── admin.html              # Панель администратора
│   ├── api.js                  # API клиент
│   ├── INTEGRATION_GUIDE.md    # Руководство по интеграции
│   └── ...
│
└── README.md                    # Этот файл
```

## 🚀 Быстрый старт

### 1. Запуск бэкенда

#### Windows:
```bash
cd back
start.bat
```

#### Linux/Mac:
```bash
cd back
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py init_admin
python manage.py runserver
```

Бэкенд будет доступен на: **http://127.0.0.1:8000**

### 2. Запуск фронтенда

Просто откройте `front/index.html` в браузере или используйте любой локальный веб-сервер:

```bash
cd front
python -m http.server 8080
```

Фронтенд будет доступен на: **http://127.0.0.1:8080**

### 3. Вход в систему

#### Для администратора:
- **Логин:** Kvv
- **Пароль:** Kvv08072001
- После входа в меню появится кнопка "Панель администратора"

#### Для обычных пользователей:
1. Нажмите "Регистрация"
2. Создайте аккаунт
3. Дождитесь одобрения администратора
4. Войдите в систему

## 📚 API Документация

### Авторизация

#### Регистрация
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "user123",
  "password": "secure_password",
  "password_confirm": "secure_password",
  "email": "user@example.com"
}
```

#### Вход
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "Kvv",
  "password": "Kvv08072001"
}
```

**Ответ:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "Kvv",
    "is_super_admin": true,
    "status": "active"
  }
}
```

#### Выход
```http
POST /api/auth/logout/
Authorization: Bearer <access_token>
```

### Администрирование (только для супер-админа)

#### Получить статистику
```http
GET /api/admin/stats/
Authorization: Bearer <access_token>
```

#### Список пользователей
```http
GET /api/users/
GET /api/users/?status=pending
Authorization: Bearer <access_token>
```

#### Одобрить пользователя
```http
POST /api/users/{id}/approve/
Authorization: Bearer <access_token>
```

#### Заблокировать пользователя
```http
POST /api/users/{id}/suspend/
Authorization: Bearer <access_token>
```

#### Разблокировать пользователя
```http
POST /api/users/{id}/unsuspend/
Authorization: Bearer <access_token>
```

#### Установить срок доступа
```http
POST /api/users/{id}/set_access_period/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "access_until": "2024-12-31T23:59:59Z"
}
```

#### Удалить пользователя
```http
DELETE /api/users/{id}/
Authorization: Bearer <access_token>
```

### Комнаты, кровати, жильцы

#### Комнаты
```http
GET /api/rooms/
POST /api/rooms/
PUT /api/rooms/{id}/
DELETE /api/rooms/{id}/
Authorization: Bearer <access_token>
```

#### Кровати
```http
GET /api/beds/
GET /api/beds/?room={room_id}
POST /api/beds/
PUT /api/beds/{id}/
DELETE /api/beds/{id}/
Authorization: Bearer <access_token>
```

#### Жильцы
```http
GET /api/residents/
GET /api/residents/?room={room_id}
GET /api/residents/?current=true
POST /api/residents/
PUT /api/residents/{id}/
DELETE /api/residents/{id}/
Authorization: Bearer <access_token>
```

#### Журнал аудита
```http
GET /api/audit-logs/
GET /api/audit-logs/?user={user_id}
GET /api/audit-logs/?action=login
Authorization: Bearer <access_token>
```

## 🔐 Безопасность

### Реализованные меры безопасности:

1. **JWT авторизация**
   - Access токен на 30 дней
   - Refresh токен на 90 дней
   - Автоматическая ротация токенов

2. **Хэширование паролей**
   - PBKDF2 алгоритм с SHA256
   - 260,000 итераций
   - Уникальная соль для каждого пароля

3. **CSRF защита**
   - Django CSRF токены
   - HTTP-only cookies

4. **XSS защита**
   - Content Security Policy headers
   - X-Content-Type-Options: nosniff
   - X-Frame-Options: DENY

5. **Журнал аудита**
   - Логирование всех действий
   - Сохранение IP адресов
   - Временные метки

6. **Разграничение прав**
   - Супер-администратор
   - Обычные пользователи
   - Гостевой доступ (регистрация)

7. **Защита от оффлайн использования**
   - Все запросы требуют валидный токен
   - Токены проверяются на сервере
   - Невозможно использовать без сервера

## 🛠️ Технологии

### Backend:
- **Django 4.2** - Web framework
- **Django REST Framework 3.14** - RESTful API
- **Django CORS Headers** - CORS support
- **SimpleJWT** - JWT authentication
- **SQLite** - Database (можно заменить на PostgreSQL/MySQL)
- **Python 3.8+**

### Frontend:
- **HTML5/CSS3/JavaScript**
- **Tailwind CSS** - Styling
- **Fetch API** - HTTP requests
- **LocalStorage** - Token storage
- **Responsive Design** - Mobile-friendly

## 📝 Модели данных

### CustomUser
- Расширенная модель пользователя
- Поля: username, email, status, access_until, is_super_admin

### Room
- Комнаты хостела
- Поля: name, description, created_by

### Bed
- Кровати в комнатах
- Поля: room, bed_type, side, bed_number, is_occupied

### Resident
- Жильцы хостела
- Поля: name, room, bed, check_in_date, check_out_date, payment_amount, payment_status

### AuditLog
- Журнал действий
- Поля: user, action, details, ip_address, timestamp

## 🌍 Многоязычность

Поддерживаемые языки:
- 🇷🇺 Русский
- 🇺🇿 O'zbek (Узбекский)
- 🇺🇸 English (Английский)

## 📱 Адаптивность

- ✅ Desktop (1920px+)
- ✅ Laptop (1024px+)
- ✅ Tablet (768px+)
- ✅ Mobile (320px+)

## 🐛 Troubleshooting

### Бэкенд не запускается

**Проблема:** `ModuleNotFoundError`
```bash
# Решение:
pip install -r requirements.txt
```

**Проблема:** `django.db.utils.OperationalError`
```bash
# Решение:
python manage.py makemigrations
python manage.py migrate
```

### CORS ошибки

**Проблема:** `Access-Control-Allow-Origin` error

**Решение:** Убедитесь что в `settings.py` установлено:
```python
CORS_ALLOW_ALL_ORIGINS = True
```

### Ошибки авторизации

**Проблема:** 401 Unauthorized

**Решение:**
1. Очистите localStorage
2. Выйдите и войдите заново
3. Проверьте что токен не истёк

## 📄 Лицензия

Этот проект создан для управления хостелом.

## 👨‍💻 Разработка

Для разработки:

1. Клонируйте репозиторий
2. Установите зависимости
3. Запустите бэкенд
4. Откройте фронтенд
5. Начните разработку

### Полезные команды:

```bash
# Создать миграции
python manage.py makemigrations

# Применить миграции
python manage.py migrate

# Создать супер-админа
python manage.py init_admin

# Запустить тесты
python manage.py test

# Собрать статику
python manage.py collectstatic

# Создать дамп БД
python manage.py dumpdata > db.json

# Загрузить дамп БД
python manage.py loaddata db.json
```

## 📧 Контакты

Для вопросов и предложений создайте Issue в репозитории.

---

**Создано с ❤️ для управления хостелами**
