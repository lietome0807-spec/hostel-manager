# ⚡ БЫСТРЫЙ ДЕПЛОЙ - 10 МИНУТ

## 🎯 САМЫЙ ПРОСТОЙ СПОСОБ

### ШАГ 1: Фронтенд на Netlify (2 минуты)

1. Откройте https://www.netlify.com/
2. Зарегистрируйтесь
3. **Перетащите папку `front`** в окно браузера
4. Готово! Скопируйте URL (например: `https://my-hostel.netlify.app`)

---

### ШАГ 2: Бэкенд на Render (8 минут)

#### A. Установите Git (если нет)
- https://git-scm.com/download/win
- Установите и перезапустите VS Code

#### B. Зарегистрируйтесь на GitHub
- https://github.com/signup

#### C. Загрузите код на GitHub

Откройте терминал в VS Code (`Ctrl + ~`):

```bash
cd C:\Users\IIoxyuCT\Desktop\HostelManager
git init
git add .
git commit -m "Initial commit"
```

На GitHub:
1. New repository → `hostel-manager`
2. Create repository
3. Скопируйте команды из "push an existing repository"
4. Вставьте в терминал

#### D. Задеплойте на Render

1. https://render.com/ → Зарегистрируйтесь
2. New → Web Service
3. Connect GitHub → выберите `hostel-manager`
4. Настройки:
   ```
   Root Directory: back
   Build Command: ./build.sh
   Start Command: gunicorn hostel_project.wsgi:application
   ```
5. Advanced → Add Environment Variable:
   ```
   SECRET_KEY: [Generate]
   DEBUG: False
   PYTHON_VERSION: 3.11.0
   ```
6. Create Web Service

#### E. Создайте базу данных

1. New → PostgreSQL
2. Name: `hostel-db`
3. Create Database
4. Скопируйте "Internal Database URL"

#### F. Подключите базу

1. В Web Service → Environment
2. Add:
   ```
   DATABASE_URL: [вставьте Internal Database URL]
   ```
3. Save → Render передеплоит

---

### ШАГ 3: Соедините фронт и бэк

#### A. Скопируйте URL бэкенда
- Например: `https://hostel-manager-api.onrender.com`

#### B. Обновите api.js

Откройте `front/api.js` (строка 6):

```javascript
// БЫЛО:
: 'https://your-backend-url.onrender.com/api';

// СТАЛО:
: 'https://hostel-manager-api.onrender.com/api';
```

#### C. Обновите на Netlify

1. На Netlify → Deploys → Drag and drop
2. Перетащите папку `front` снова
3. Готово!

---

## ✅ ПРОВЕРКА

1. Откройте ваш Netlify URL
2. Попробуйте войти:
   - Логин: `Kvv`
   - Пароль: `Kvv08072001`
3. Если работает → **УСПЕХ!** 🎉

---

## 📝 ВАЖНО

- Бэкенд "засыпает" после 15 мин → первый запрос медленный
- PostgreSQL бесплатна 90 дней
- Фронтенд на Netlify бесплатен навсегда

---

## 🆘 ПРОБЛЕМЫ?

1. **Бэкенд не деплоится:**
   - Проверьте логи в Render
   - Убедитесь что `Root Directory: back`

2. **CORS ошибки:**
   - Подождите 2-3 минуты после деплоя
   - Проверьте что URL в api.js правильный

3. **База не подключается:**
   - Используйте Internal Database URL
   - Проверьте что DATABASE_URL добавлен

---

**Подробная инструкция:** `back/RENDER_DEPLOY.md`

**Удачи!** 🚀
