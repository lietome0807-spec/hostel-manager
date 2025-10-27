# 🚀 ДЕПЛОЙ БЭКЕНДА НА RENDER.COM

## ✅ ВСЁ ГОТОВО! Теперь деплоим!

---

## 📋 ВАРИАНТ 1: ЧЕРЕЗ GITHUB (РЕКОМЕНДУЮ)

### ШАГ 1: Установите Git

1. **Скачайте Git:** https://git-scm.com/download/win
2. **Установите** с настройками по умолчанию
3. **Перезапустите** VS Code

### ШАГ 2: Создайте GitHub аккаунт

1. Зайдите на **https://github.com/signup**
2. Зарегистрируйтесь

### ШАГ 3: Создайте репозиторий на GitHub

1. На GitHub: **New repository**
2. Имя: `hostel-manager`
3. Приватность: **Public** или **Private**
4. **Create repository**

### ШАГ 4: Загрузите код на GitHub

Откройте терминал в папке `HostelManager`:

```bash
cd C:\Users\IIoxyuCT\Desktop\HostelManager

# Инициализируем Git
git init

# Добавляем все файлы
git add .

# Делаем первый коммит
git commit -m "Initial commit"

# Подключаем к GitHub (замените YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/hostel-manager.git

# Загружаем
git branch -M main
git push -u origin main
```

### ШАГ 5: Деплой на Render

1. **Зайдите на https://render.com/**
2. **Зарегистрируйтесь** (можно через GitHub)
3. **Dashboard → New → Web Service**
4. **Connect GitHub**
5. **Выберите репозиторий** `hostel-manager`
6. **Настройки:**
   ```
   Name: hostel-manager-api
   Region: Frankfurt (EU Central)
   Branch: main
   Root Directory: back
   Runtime: Python 3
   Build Command: ./build.sh
   Start Command: gunicorn hostel_project.wsgi:application
   ```
7. **Instance Type:** Free
8. **Advanced → Environment Variables:**
   ```
   SECRET_KEY = [Generate] (нажмите кнопку Generate)
   DEBUG = False
   PYTHON_VERSION = 3.11.0
   ```
9. **Create Web Service**

### ШАГ 6: Создайте PostgreSQL базу

1. **Dashboard → New → PostgreSQL**
2. **Настройки:**
   ```
   Name: hostel-db
   Region: Frankfurt (EU Central)
   PostgreSQL Version: 16
   ```
3. **Instance Type:** Free
4. **Create Database**
5. **Скопируйте Internal Database URL**

### ШАГ 7: Подключите базу к сервису

1. Вернитесь в **Web Service → Environment**
2. **Add Environment Variable:**
   ```
   DATABASE_URL = [вставьте Internal Database URL]
   ```
3. **Save Changes**
4. **Render автоматически передеплоит**

### ШАГ 8: Подождите деплоя

- Следите за логами в Render
- Деплой займет ~5-10 минут
- Когда увидите "Build successful" → готово!

### ШАГ 9: Проверьте API

1. Скопируйте URL сервиса (например: `https://hostel-manager-api.onrender.com`)
2. Откройте в браузере: `https://hostel-manager-api.onrender.com/api/`
3. Должна открыться страница API
4. Проверьте документацию: `https://hostel-manager-api.onrender.com/admin/`

---

## 📋 ВАРИАНТ 2: БЕЗ GITHUB (ЧЕРЕЗ GIT URL)

Если не хотите регистрироваться на GitHub:

1. **Загрузите код на любой Git сервис:**
   - GitLab.com
   - Bitbucket.org
   
2. **На Render → New → Web Service**
3. **Public Git Repository** → вставьте URL

---

## 🔄 КАК ОБНОВЛЯТЬ КОД

### Если используете GitHub:

```bash
cd C:\Users\IIoxyuCT\Desktop\HostelManager

# Внесите изменения в код
# Затем:

git add .
git commit -m "Описание изменений"
git push

# Render автоматически передеплоит!
```

---

## ⚙️ ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ (Environment Variables)

В Render обязательно установите:

```
SECRET_KEY = [generate random string]
DEBUG = False
DATABASE_URL = [Internal Database URL из PostgreSQL]
PYTHON_VERSION = 3.11.0
ALLOWED_HOSTS = your-app.onrender.com
```

Опционально:

```
CORS_ALLOWED_ORIGINS = https://your-frontend.netlify.app
```

---

## 🆘 TROUBLESHOOTING

### Ошибка при build:

```
ERROR: Could not find a version that satisfies the requirement
```

**Решение:** Проверьте `requirements.txt`, все пакеты должны быть доступны

### Ошибка с базой данных:

```
django.db.utils.OperationalError: FATAL: password authentication failed
```

**Решение:** 
1. Проверьте что DATABASE_URL правильный
2. Используйте **Internal Database URL**, не External

### Build успешен, но сайт не работает:

```
Application failed to respond
```

**Решение:**
1. Проверьте **Start Command**: `gunicorn hostel_project.wsgi:application`
2. Проверьте **Root Directory**: `back`
3. Проверьте логи в Render

### Статика не загружается:

**Решение:** WhiteNoise должен быть в middleware (уже добавлено)

---

## 💡 СОВЕТЫ

1. **Free план Render "засыпает"** после 15 минут бездействия
   - Первый запрос после сна будет медленным (30-60 сек)
   - Это нормально для бесплатного плана

2. **PostgreSQL Free** работает 90 дней бесплатно
   - После этого нужно либо оплатить, либо создать новую базу

3. **Логи** - ваш лучший друг:
   - Render → вашsервис → Logs
   - Там видно всё что происходит

4. **Ручной деплой:**
   - Render → ваш сервис → Manual Deploy → Deploy latest commit

---

## 🎉 ГОТОВО!

После успешного деплоя:

1. Скопируйте URL бэкенда
2. Вставьте в `front/api.js` (строка 6)
3. Задеплойте фронт на Netlify
4. Всё работает! 🚀

---

## 📞 ПОДДЕРЖКА

Если что-то не работает:

1. Проверьте логи в Render
2. Проверьте переменные окружения
3. Убедитесь что DATABASE_URL правильный
4. Попробуйте Manual Deploy

**Удачи!** 💪
