# 🚀 Инструкция по деплою на GitHub Pages

## Шаг 1: Подготовка репозитория

1. **Создайте новый репозиторий на GitHub:**
   - Перейдите на https://github.com/new
   - Назовите репозиторий `rasp` (или любое другое имя)
   - Сделайте репозиторий публичным
   - Не добавляйте README, .gitignore или лицензию (они уже есть)

2. **Инициализируйте git в папке frontend:**
   ```bash
   cd /Users/alex/Desktop/rasp/rasp/frontend
   git init
   git add .
   git commit -m "Initial commit: React app for MAI schedule download"
   ```

3. **Добавьте удаленный репозиторий:**
   ```bash
   git remote add origin https://github.com/yourusername/rasp.git
   git branch -M main
   git push -u origin main
   ```

## Шаг 2: Настройка GitHub Pages

1. **Обновите homepage в package.json:**
   ```json
   "homepage": "https://yourusername.github.io/rasp"
   ```
   Замените `yourusername` на ваш GitHub username.

2. **Деплой на GitHub Pages:**
   ```bash
   npm run deploy
   ```

3. **Настройте GitHub Pages в настройках репозитория:**
   - Перейдите в ваш репозиторий на GitHub
   - Нажмите на вкладку "Settings"
   - Прокрутите вниз до раздела "Pages"
   - В разделе "Source" выберите "Deploy from a branch"
   - В разделе "Branch" выберите "gh-pages" и папку "/ (root)"
   - Нажмите "Save"

## Шаг 3: Проверка деплоя

1. **Дождитесь завершения деплоя** (обычно 1-2 минуты)
2. **Откройте ваш сайт** по адресу: `https://yourusername.github.io/rasp`
3. **Проверьте функциональность:**
   - Выбор института
   - Выбор курса и уровня образования
   - Выбор группы
   - Скачивание файла .ics

## Шаг 4: Обновление данных

Когда нужно обновить список групп или расписания:

1. **Обновите данные Python скриптами:**
   ```bash
   cd /Users/alex/Desktop/rasp/rasp
   python main.py
   ```

2. **Скопируйте обновленные файлы:**
   ```bash
   cp groups/groups.json frontend/public/
   cp rasp/*.ics frontend/public/rasp/
   ```

3. **Зафиксируйте изменения и задеплойте:**
   ```bash
   cd frontend
   git add .
   git commit -m "Update schedule data"
   git push origin main
   npm run deploy
   ```

## 🔧 Troubleshooting

### Проблема: Сайт не открывается
- Убедитесь, что branch "gh-pages" создался
- Проверьте, что в настройках Pages выбран правильный branch
- Подождите несколько минут после деплоя

### Проблема: Файлы не скачиваются
- Убедитесь, что файлы .ics скопированы в `public/rasp/`
- Проверьте, что пути к файлам правильные

### Проблема: Данные групп не загружаются
- Убедитесь, что файл `groups.json` находится в `public/`
- Проверьте консоль браузера на ошибки

## 📝 Полезные команды

```bash
# Локальный запуск
npm run dev

# Сборка для продакшена
npm run build

# Предварительный просмотр сборки
npm run preview

# Деплой на GitHub Pages
npm run deploy

# Проверка статуса git
git status

# Просмотр логов
git log --oneline
```

## 🌐 Настройка кастомного домена (опционально)

Если хотите использовать свой домен:

1. **Добавьте файл CNAME в public:**
   ```bash
   echo "yourdomain.com" > public/CNAME
   ```

2. **Настройте DNS записи:**
   - A запись: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - CNAME запись: `www` → `yourusername.github.io`

3. **Включите кастомный домен в настройках GitHub Pages**
