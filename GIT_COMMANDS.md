# 📝 GIT КОМАНДЫ - ШПАРГАЛКА

## 🚀 ПЕРВАЯ ЗАГРУЗКА НА GITHUB

```bash
# 1. Перейти в папку проекта
cd C:\Users\IIoxyuCT\Desktop\HostelManager

# 2. Инициализировать Git
git init

# 3. Добавить все файлы
git add .

# 4. Сделать первый коммит
git commit -m "Initial commit - Hostel Manager"

# 5. Подключить к GitHub (ЗАМЕНИТЕ YOUR_USERNAME!)
git remote add origin https://github.com/YOUR_USERNAME/hostel-manager.git

# 6. Переименовать ветку в main
git branch -M main

# 7. Загрузить на GitHub
git push -u origin main
```

---

## 🔄 ОБНОВЛЕНИЕ КОДА (после изменений)

```bash
# 1. Перейти в папку
cd C:\Users\IIoxyuCT\Desktop\HostelManager

# 2. Посмотреть что изменилось
git status

# 3. Добавить все изменения
git add .

# 4. Сделать коммит с описанием
git commit -m "Описание что вы изменили"

# 5. Загрузить на GitHub
git push
```

**Render автоматически задеплоит новую версию!**

---

## 📋 ЧАСТЫЕ КОМАНДЫ

### Проверить статус
```bash
git status
```

### Посмотреть историю
```bash
git log
```

### Отменить изменения (до commit)
```bash
git checkout .
```

### Посмотреть удаленные репозитории
```bash
git remote -v
```

---

## 🆘 РЕШЕНИЕ ПРОБЛЕМ

### "not a git repository"
```bash
git init
```

### "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/hostel-manager.git
```

### Забыли добавить файл
```bash
git add название_файла.py
git commit --amend --no-edit
git push -f
```

### Хотите начать заново
```bash
rm -rf .git
git init
git add .
git commit -m "Fresh start"
```

---

## 💡 СОВЕТЫ

1. **Делайте commit часто** - после каждой важной фичи
2. **Пишите понятные сообщения** - "Добавил календарь" лучше чем "fix"
3. **Делайте push минимум раз в день** - чтобы не потерять код
4. **Перед большими изменениями** - сделайте commit текущего состояния

---

## 📱 ПРИМЕРЫ ХОРОШИХ COMMIT СООБЩЕНИЙ

```bash
git commit -m "Добавил админ-панель с календарем"
git commit -m "Исправил баг с блокировкой пользователей"
git commit -m "Улучшил дизайн карточек"
git commit -m "Добавил автоблокировку истекших пользователей"
git commit -m "Обновил requirements.txt для Render"
```

---

## 🎯 WORKFLOW

```
1. Работаете над кодом
   ↓
2. git add .
   ↓
3. git commit -m "Что сделали"
   ↓
4. git push
   ↓
5. Render автоматически деплоит
   ↓
6. Проверяете что работает
   ↓
7. Повторяете с шага 1
```

---

**Это всё что нужно знать!** 💪
