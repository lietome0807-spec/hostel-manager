# 🚀 ИНСТРУКЦИЯ ПО ДЕПЛОЮ HOSTEL MANAGER

## 📦 СТРУКТУРА ПРОЕКТА

```
HostelManager/
├── front/               # Фронтенд (HTML/CSS/JS)
│   ├── index.html
│   ├── admin.html
│   ├── api.js
│   ├── netlify.toml
│   └── _redirects
└── back/                # Бэкенд (FastAPI/Python)
    ├── main.py
    ├── requirements.txt
    └── ...
```

---

## 🌐 ДЕПЛОЙ ФРОНТЕНДА НА NETLIFY

### Вариант 1: Drag & Drop (САМЫЙ ПРОСТОЙ) ⭐

1. **Зайдите на https://www.netlify.com/**
2. **Зарегистрируйтесь/войдите** (можно через GitHub)
3. **Перейдите на Dashboard**
4. **Перетащите папку `front`** в окно "Drag and drop your site output folder here"
5. **Готово!** Ваш сайт будет доступен по адресу типа `https://random-name-123.netlify.app`

### Вариант 2: Через Git/GitHub (АВТОДЕПЛОЙ)

1. **Установите Git:**
   - Скачайте: https://git-scm.com/download/win
   - Установите с настройками по умолчанию

2. **Создайте GitHub аккаунт:**
   - https://github.com/signup

3. **Создайте репозиторий:**
   ```bash
   cd C:\Users\IIoxyuCT\Desktop\HostelManager
   git init
   git add .
   git commit -m "Initial commit"
   ```

4. **Загрузите на GitHub:**
   - Создайте новый репозиторий на GitHub
   - Следуйте инструкциям GitHub для push

5. **Подключите к Netlify:**
   - На Netlify: "Add new site" → "Import an existing project"
   - Выберите GitHub
   - Выберите ваш репозиторий
   - Build settings:
     - Base directory: `front`
     - Build command: (оставьте пустым)
     - Publish directory: `.`
   - Deploy!

### ⚙️ Настройка переменных окружения

После деплоя бэкенда:

1. В Netlify: Site settings → Environment variables
2. Добавьте:
   - `API_URL` = URL вашего бэкенда (например: `https://your-app.onrender.com`)

---

## 🔧 ДЕПЛОЙ БЭКЕНДА НА RENDER.COM

### ШАГ 1: Подготовка

1. **Убедитесь что в папке `back` есть:**
   - `requirements.txt` (зависимости Python)
   - `main.py` (точка входа)

2. **Создайте файл `render.yaml`** в корне проекта:
   ```yaml
   services:
     - type: web
       name: hostel-manager-api
       env: python
       buildCommand: "pip install -r requirements.txt"
       startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
       envVars:
         - key: DATABASE_URL
           fromDatabase:
             name: hostel-db
             property: connectionString
         - key: SECRET_KEY
           generateValue: true
   
   databases:
     - name: hostel-db
       databaseName: hostel_manager
       user: hostel_user
   ```

### ШАГ 2: Деплой на Render

1. **Зайдите на https://render.com/**
2. **Зарегистрируйтесь** (можно через GitHub)
3. **Создайте Web Service:**
   - Dashboard → New → Web Service
   - Connect repository (или введите Git URL)
   - Settings:
     - Name: `hostel-manager-api`
     - Environment: `Python 3`
     - Build Command: `pip install -r back/requirements.txt`
     - Start Command: `cd back && uvicorn main:app --host 0.0.0.0 --port $PORT`
     - Instance Type: `Free`

4. **Создайте PostgreSQL базу:**
   - Dashboard → New → PostgreSQL
   - Name: `hostel-db`
   - Plan: `Free`
   - Создайте

5. **Подключите базу к сервису:**
   - В настройках Web Service → Environment
   - Добавьте переменную `DATABASE_URL`
   - Значение: скопируйте Internal Database URL из настроек PostgreSQL

6. **Deploy!**

### ШАГ 3: Обновите фронтенд

1. Скопируйте URL вашего бэкенда (например: `https://hostel-manager-api.onrender.com`)
2. Откройте `front/api.js`
3. Замените:
   ```javascript
   : 'https://your-backend-url.onrender.com/api';
   ```
   на:
   ```javascript
   : 'https://hostel-manager-api.onrender.com/api';
   ```
4. Загрузите обновленный фронт на Netlify

---

## 🎯 АЛЬТЕРНАТИВНЫЕ ВАРИАНТЫ ХОСТИНГА БЭКЕНДА

### 1. Railway.app 🚂
```
Плюсы:
✅ $5/месяц бесплатно
✅ Простой деплой
✅ PostgreSQL включена
✅ Быстрый

Минусы:
❌ Лимит часов работы

Инструкция:
1. https://railway.app/
2. New Project → Deploy from GitHub
3. Add PostgreSQL
4. Add переменные окружения
5. Deploy
```

### 2. Fly.io ✈️
```
Плюсы:
✅ Бесплатный план
✅ Быстрый
✅ Много локаций

Минусы:
❌ Сложнее настроить
❌ Требует flyctl CLI

Инструкция:
1. https://fly.io/
2. Установите flyctl
3. fly launch
4. fly deploy
```

### 3. PythonAnywhere 🐍
```
Плюсы:
✅ Специально для Python
✅ Простая настройка
✅ Бесплатный план

Минусы:
❌ Медленнее
❌ Ограничения базы данных

Инструкция:
1. https://www.pythonanywhere.com/
2. Create account
3. Upload code
4. Setup Web app
5. Configure WSGI
```

---

## 🔄 CORS (ВАЖНО!)

В вашем `back/main.py` должно быть:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-site.netlify.app",  # Ваш Netlify URL
        "http://localhost:3000",           # Для локальной разработки
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## ✅ ПРОВЕРКА ПОСЛЕ ДЕПЛОЯ

### Фронтенд:
1. Откройте ваш Netlify URL
2. Проверьте что страница загружается
3. Откройте DevTools (F12) → Console
4. Не должно быть ошибок CORS

### Бэкенд:
1. Откройте `https://your-backend.onrender.com/docs`
2. Должна открыться Swagger документация API
3. Попробуйте тестовые запросы

### Полная проверка:
1. Зарегистрируйтесь на фронтенде
2. Войдите в систему
3. Создайте комнату
4. Проверьте админ-панель

---

## 🆘 TROUBLESHOOTING

### Ошибка CORS:
```
Access to fetch at '...' from origin '...' has been blocked by CORS policy
```
**Решение:** Добавьте ваш Netlify URL в allow_origins в бэкенде

### Ошибка 404 на API:
```
GET https://your-api.com/api/users/ 404
```
**Решение:** Проверьте что бэкенд запущен и URL правильный

### Бэкенд "засыпает":
```
Первый запрос после паузы очень медленный
```
**Решение:** Это нормально для бесплатного плана Render. Платные планы не засыпают.

### База данных не подключается:
```
FATAL: password authentication failed
```
**Решение:** Проверьте DATABASE_URL в переменных окружения

---

## 📱 БЫСТРЫЙ СТАРТ

**МИНИМУМ ДЛЯ РАБОТЫ ТОЛЬКО С LOCALSTORAGE:**

Если вы хотите чтобы всё работало БЕЗ бэкенда (только localStorage):

1. Деплойте только `front` на Netlify
2. В `api.js` закомментируйте все API вызовы
3. Всё будет работать локально в браузере!

**Плюсы:**
✅ Бесплатно
✅ Быстро
✅ Просто

**Минусы:**
❌ Данные только в браузере
❌ Нет синхронизации между устройствами
❌ Данные теряются при очистке браузера

---

## 💰 СТОИМОСТЬ

### Вариант 1: ПОЛНОСТЬЮ БЕСПЛАТНО
```
Netlify (фронт):     $0/месяц
Render.com (бэк):    $0/месяц
PostgreSQL:          $0/месяц (90 дней)

ИТОГО: $0/месяц
```

### Вариант 2: ТОЛЬКО ФРОНТ (localStorage)
```
Netlify:             $0/месяц

ИТОГО: $0/месяц
```

### Вариант 3: СТАБИЛЬНЫЙ (рекомендую для продакшна)
```
Netlify:             $0/месяц
Railway:             $5-10/месяц
PostgreSQL:          Включена

ИТОГО: $5-10/месяц
```

---

## 🎓 ПОЛЕЗНЫЕ ССЫЛКИ

- **Netlify Docs:** https://docs.netlify.com/
- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app/
- **FastAPI Deployment:** https://fastapi.tiangolo.com/deployment/

---

## 📞 ПОДДЕРЖКА

Если что-то не работает - проверьте:
1. DevTools Console (F12)
2. Network tab (запросы)
3. Логи на Render/Railway
4. CORS настройки

---

**Удачи с деплоем!** 🚀
