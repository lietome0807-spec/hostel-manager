# 🔧 Устранение неполадок - Hostel Manager

## ❌ Ошибка запроса (Request Error)

### Возможные причины:

---

## 1️⃣ Бэкенд не запущен

**Симптомы:**
- "Failed to fetch"
- "Network Error"
- "ERR_CONNECTION_REFUSED"

**Решение:**

1. Откройте терминал в папке `back`
2. Запустите бэкенд:
   ```bash
   # Windows
   start.bat
   
   # Linux/Mac
   ./start.sh
   ```

3. Убедитесь что сервер запустился на порту 8000:
   ```
   Starting development server at http://127.0.0.1:8000/
   ```

4. Проверьте доступность в браузере: http://127.0.0.1:8000/api/

---

## 2️⃣ Неправильный URL API

**Симптомы:**
- "404 Not Found"
- "Endpoint not found"

**Решение:**

Проверьте в файле `front/api.js`:
```javascript
const API_BASE_URL = 'http://127.0.0.1:8000/api';
```

Если бэкенд на другом порту, измените URL.

---

## 3️⃣ CORS ошибки

**Симптомы:**
- "CORS policy blocked"
- "Access-Control-Allow-Origin"

**Решение:**

1. Откройте `back/hostel_project/settings.py`
2. Убедитесь что есть:
   ```python
   CORS_ALLOW_ALL_ORIGINS = True
   CORS_ALLOW_CREDENTIALS = True
   ```

3. Перезапустите бэкенд

---

## 4️⃣ Порт занят

**Симптомы:**
- "Error: That port is already in use"
- Бэкенд не запускается

**Решение:**

**Windows:**
```bash
# Найти процесс на порту 8000
netstat -ano | findstr :8000

# Убить процесс (замените PID)
taskkill /PID <PID> /F

# Или запустить на другом порту
python manage.py runserver 8001
```

**Linux/Mac:**
```bash
# Найти процесс
lsof -i :8000

# Убить процесс
kill -9 <PID>
```

---

## 5️⃣ Зависимости не установлены

**Симптомы:**
- "ModuleNotFoundError"
- "No module named 'rest_framework'"

**Решение:**
```bash
cd back
pip install -r requirements.txt
```

---

## 6️⃣ Миграции не применены

**Симптомы:**
- "no such table"
- "OperationalError"

**Решение:**
```bash
cd back
python manage.py makemigrations
python manage.py migrate
```

---

## 7️⃣ Токен истёк

**Симптомы:**
- "401 Unauthorized"
- "Token expired"

**Решение:**

1. Откройте консоль браузера (F12)
2. Выполните:
   ```javascript
   localStorage.clear()
   ```
3. Обновите страницу
4. Войдите заново

---

## 8️⃣ Супер-админ не создан

**Симптомы:**
- Не можете войти с Kvv/Kvv08072001

**Решение:**
```bash
cd back
python manage.py init_admin
```

---

## 🛠️ Пошаговая диагностика:

### Шаг 1: Проверка бэкенда

Откройте http://127.0.0.1:8000/api/ в браузере

**Ожидаемый результат:**
```json
{
    "rooms": "http://127.0.0.1:8000/api/rooms/",
    "beds": "http://127.0.0.1:8000/api/beds/",
    ...
}
```

**Если не открывается** → Бэкенд не запущен

---

### Шаг 2: Проверка консоли браузера

1. Откройте фронтенд
2. Нажмите F12
3. Перейдите во вкладку Console
4. Попробуйте войти
5. Смотрите ошибки

**Типичные ошибки:**

❌ **"Failed to fetch"**
```
Решение: Запустите бэкенд
```

❌ **"CORS policy"**
```
Решение: Проверьте CORS настройки в settings.py
```

❌ **"401 Unauthorized"**
```
Решение: Очистите localStorage и войдите заново
```

❌ **"404 Not Found"**
```
Решение: Проверьте URL в api.js
```

---

### Шаг 3: Проверка Network

1. Откройте F12 → вкладка Network
2. Попробуйте войти
3. Найдите запрос к `/api/auth/login/`
4. Посмотрите:
   - **Status Code** (должен быть 200)
   - **Response** (ответ сервера)
   - **Request URL** (правильный ли адрес)

---

## 📝 Частые ошибки и решения:

### Ошибка: "Неверный логин или пароль"

**Причина:** Супер-админ не создан

**Решение:**
```bash
cd back
python manage.py init_admin
```

---

### Ошибка: "Необходима авторизация"

**Причина:** Токен не сохранён или истёк

**Решение:**
```javascript
// В консоли браузера (F12)
localStorage.clear()
// Затем войдите заново
```

---

### Ошибка: "Account is waiting for administrator confirmation"

**Причина:** Пользователь не одобрен админом

**Решение:**
1. Войдите как админ (Kvv/Kvv08072001)
2. Откройте панель администратора
3. Одобрите пользователя

---

### Ошибка: "Пароли не совпадают"

**Причина:** При регистрации пароли не совпадают

**Решение:** Введите одинаковые пароли в оба поля

---

## 🔍 Продвинутая диагностика:

### Проверка API вручную:

**1. Тест регистрации:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123","password_confirm":"test123"}'
```

**2. Тест входа:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"Kvv","password":"Kvv08072001"}'
```

**3. Тест статистики:**
```bash
curl http://127.0.0.1:8000/api/admin/stats/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📊 Лог-файлы:

### Django логи:

Смотрите в терминале где запущен бэкенд. Там будут все запросы и ошибки.

### Браузерные логи:

1. F12 → Console - JavaScript ошибки
2. F12 → Network - HTTP запросы
3. F12 → Application → Local Storage - Токены

---

## 🚨 Экстренные меры:

### Полный сброс:

```bash
# 1. Остановите бэкенд (Ctrl+C)

# 2. Удалите базу данных
cd back
rm db.sqlite3

# 3. Пересоздайте базу
python manage.py makemigrations
python manage.py migrate
python manage.py init_admin

# 4. Очистите браузер
# F12 → Console:
localStorage.clear()

# 5. Перезапустите бэкенд
python manage.py runserver

# 6. Обновите страницу фронтенда
```

---

## 📞 Контрольный список:

Проверьте всё по порядку:

- [ ] Python 3.8+ установлен
- [ ] Зависимости установлены (`pip install -r requirements.txt`)
- [ ] Миграции применены (`python manage.py migrate`)
- [ ] Супер-админ создан (`python manage.py init_admin`)
- [ ] Бэкенд запущен (`python manage.py runserver`)
- [ ] Порт 8000 свободен
- [ ] CORS настроен (`CORS_ALLOW_ALL_ORIGINS = True`)
- [ ] Браузер не блокирует запросы
- [ ] localStorage доступен
- [ ] api.js подключён в index.html

---

## 💡 Советы:

1. **Всегда проверяйте консоль браузера** (F12) - там видны все ошибки
2. **Смотрите терминал бэкенда** - там видны все запросы
3. **Используйте инкогнито режим** - чтобы исключить проблемы с кэшем
4. **Проверяйте Network вкладку** - чтобы видеть HTTP запросы

---

## ✅ Тест успешной работы:

Если всё работает правильно:

1. ✅ Бэкенд отвечает на http://127.0.0.1:8000/api/
2. ✅ Можете войти с Kvv/Kvv08072001
3. ✅ Открывается панель администратора
4. ✅ Видны пользователи и статистика
5. ✅ В консоли нет красных ошибок
6. ✅ В Network все запросы со статусом 200

---

Если проблема не решена - напишите точный текст ошибки!
