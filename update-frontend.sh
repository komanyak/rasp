#!/bin/bash

# Скрипт для обновления данных в React приложении

echo "🔄 Обновление данных расписания..."

# Переходим в корневую папку проекта
cd "$(dirname "$0")"

echo "📊 Обновляем данные групп..."
# Запускаем Python скрипт для обновления данных
python main.py

echo "📁 Копируем обновленные файлы в frontend..."
# Копируем обновленные данные
cp groups/groups.json frontend/public/
cp rasp/*.ics frontend/public/rasp/

echo "✅ Данные обновлены!"
echo "🚀 Для деплоя выполните:"
echo "   cd frontend"
echo "   git add ."
echo "   git commit -m 'Update schedule data'"
echo "   git push origin main"
echo "   npm run deploy"
