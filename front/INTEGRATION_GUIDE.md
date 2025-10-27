# Руководство по интеграции фронтенда с бэкендом

## Что было создано:

### Бэкенд (Django REST API)
1. ✅ Полноценный Django бэкенд в папке `back/`
2. ✅ Модели базы данных для пользователей, комнат, кроватей, жильцов
3. ✅ REST API для всех операций
4. ✅ JWT авторизация
5. ✅ Панель администратора с полным функционалом
6. ✅ Журнал аудита всех действий
7. ✅ Защита от взлома и оффлайн использования

### Фронтенд
1. ✅ `api.js` - Клиент для работы с API
2. ✅ `admin.html` - Панель администратора
3. ✅ Ваш существующий `index.html` (требует интеграции)

## Инструкции по запуску:

### 1. Запуск бэкенда:

```bash
cd back
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py init_admin
python manage.py runserver
```

Или просто запустите `back/start.bat`

Бэкенд будет доступен на: http://127.0.0.1:8000

### 2. Добавьте в ваш index.html:

Добавьте перед закрывающим тегом `</body>`:

```html
<script src="api.js"></script>
```

### 3. Обновите функции авторизации в index.html:

Замените существующие функции `login()` и `register()` на:

```javascript
// Login function
async function login() {
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    if (!username || !password) {
        alert('Заполните все поля');
        return;
    }
    
    try {
        const result = await apiClient.login(username, password);
        document.getElementById('authScreen').style.display = 'none';
        document.getElementById('appScreen').style.display = 'block';
        
        // Update UI with user info
        const initials = username.substring(0, 2).toUpperCase();
        document.getElementById('avatarInitials').textContent = initials;
        
        // Show admin panel button if super admin
        if (apiClient.isSuperAdmin()) {
            document.getElementById('adminPanelBtn').style.display = 'block';
        }
        
        alert('Добро пожаловать!');
    } catch (error) {
        alert(error.message);
    }
}

// Register function
async function register() {
    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('registerConfirmPassword').value;
    
    if (!username || !password || !confirmPassword) {
        alert('Заполните все поля');
        return;
    }
    
    try {
        const result = await apiClient.register(username, password, confirmPassword);
        alert(result.message);
        showAuthTab('login');
    } catch (error) {
        alert(error.message);
    }
}

// Logout function
async function logout() {
    await apiClient.logout();
    document.getElementById('authScreen').style.display = 'flex';
    document.getElementById('appScreen').style.display = 'none';
}

// Open admin panel
function openAdminPanel() {
    window.open('admin.html', '_blank');
}
```

### 4. Проверка авторизации при загрузке:

Добавьте в начало скрипта в index.html:

```javascript
// Check authentication on load
window.addEventListener('DOMContentLoaded', function() {
    if (apiClient.isAuthenticated()) {
        document.getElementById('authScreen').style.display = 'none';
        document.getElementById('appScreen').style.display = 'block';
        
        const username = apiClient.user.username;
        const initials = username.substring(0, 2).toUpperCase();
        document.getElementById('avatarInitials').textContent = initials;
        
        if (apiClient.isSuperAdmin()) {
            document.getElementById('adminPanelBtn').style.display = 'block';
        }
    }
});
```

## Логин администратора:

**Логин:** Kvv  
**Пароль:** Kvv08072001

## API Endpoints:

- Регистрация: `POST /api/auth/register/`
- Вход: `POST /api/auth/login/`
- Выход: `POST /api/auth/logout/`
- Текущий пользователь: `GET /api/auth/me/`

### Для администратора:
- Статистика: `GET /api/admin/stats/`
- Пользователи: `GET /api/users/`
- Одобрить: `POST /api/users/{id}/approve/`
- Заблокировать: `POST /api/users/{id}/suspend/`
- Разблокировать: `POST /api/users/{id}/unsuspend/`
- Установить срок: `POST /api/users/{id}/set_access_period/`
- Удалить: `DELETE /api/users/{id}/`

### Комнаты, кровати, жильцы:
- Комнаты: `/api/rooms/`
- Кровати: `/api/beds/`
- Жильцы: `/api/residents/`
- Журнал: `/api/audit-logs/`

## Функционал панели администратора:

1. ✅ Просмотр всех пользователей
2. ✅ Одобрение/отклонение регистраций
3. ✅ Блокировка/разблокировка пользователей
4. ✅ Установка срока доступа
5. ✅ Удаление пользователей
6. ✅ Просмотр логинов (пароли зашифрованы)
7. ✅ Журнал всех действий с IP адресами
8. ✅ Статистика системы

## Безопасность:

1. **JWT токены** - Все запросы требуют авторизацию
2. **Хэширование паролей** - Используется PBKDF2
3. **CSRF защита** - Встроена в Django
4. **Журнал аудита** - Все действия логируются
5. **Разграничение прав** - Админ и обычные пользователи
6. **Защита от оффлайн использования** - Требуется токен от сервера

## Дополнительные возможности:

### Синхронизация данных с сервером:

Вы можете добавить синхронизацию комнат, кроватей и жильцов с сервером:

```javascript
// Save room to server
async function saveRoomToServer(room) {
    try {
        await apiClient.createRoom({
            name: room.name,
            description: room.number
        });
    } catch (error) {
        console.error('Error saving room:', error);
    }
}

// Load rooms from server
async function loadRoomsFromServer() {
    try {
        const rooms = await apiClient.getRooms();
        // Process rooms...
    } catch (error) {
        console.error('Error loading rooms:', error);
    }
}
```

## Проблемы и решения:

### CORS ошибки:
Если возникают CORS ошибки, убедитесь что бэкенд запущен и в `settings.py` установлено:
```python
CORS_ALLOW_ALL_ORIGINS = True
```

### Ошибки 401 Unauthorized:
- Проверьте что токен сохранён в localStorage
- Попробуйте выйти и войти заново

### Бэкенд не запускается:
- Убедитесь что установлен Python 3.8+
- Проверьте что все зависимости установлены: `pip install -r requirements.txt`
- Примените миграции: `python manage.py migrate`
