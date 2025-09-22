#!/bin/bash

# Скрипт для обновления расписания с логированием

echo "🔄 Начинаем обновление расписания..."
echo "📅 Время: $(date '+%Y-%m-%d %H:%M:%S')"

# Переходим в корневую папку проекта
cd "$(dirname "$0")"

# Создаем лог файл
LOG_FILE="update.log"
echo "=== Обновление расписания $(date '+%Y-%m-%d %H:%M:%S') ===" >> $LOG_FILE

echo "📊 Обновляем данные групп..."
echo "Парсинг групп..." >> $LOG_FILE
python group_parser.py >> $LOG_FILE 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Парсинг групп завершен успешно"
    echo "✅ Парсинг групп завершен успешно" >> $LOG_FILE
else
    echo "❌ Ошибка при парсинге групп"
    echo "❌ Ошибка при парсинге групп" >> $LOG_FILE
    exit 1
fi

echo "📅 Обновляем расписания..."
echo "Обновление расписаний..." >> $LOG_FILE
python main.py >> $LOG_FILE 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Обновление расписаний завершено успешно"
    echo "✅ Обновление расписаний завершено успешно" >> $LOG_FILE
else
    echo "❌ Ошибка при обновлении расписаний"
    echo "❌ Ошибка при обновлении расписаний" >> $LOG_FILE
    exit 1
fi

echo "📁 Копируем обновленные файлы в frontend..."
cp groups/groups.json frontend/public/groups.json
mkdir -p frontend/public/rasp
cp rasp/*.ics frontend/public/rasp/

# Создаем файл с информацией о последнем обновлении
echo "📝 Создаем файл информации об обновлении..."
echo '{"lastUpdated": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'", "version": "'$(date +%s)'"}' > frontend/public/update-info.json

echo "📊 Статистика обновления:"
echo "📊 Статистика обновления:" >> $LOG_FILE

# Подсчитываем количество файлов
GROUPS_COUNT=$(wc -l < groups/groups.json 2>/dev/null || echo "0")
SCHEDULE_COUNT=$(ls -1 rasp/*.ics 2>/dev/null | wc -l)
FRONTEND_SCHEDULE_COUNT=$(ls -1 frontend/public/rasp/*.ics 2>/dev/null | wc -l)

echo "  - Строк в groups.json: $GROUPS_COUNT"
echo "  - Файлов расписания: $SCHEDULE_COUNT"
echo "  - Скопировано в frontend: $FRONTEND_SCHEDULE_COUNT"

echo "  - Строк в groups.json: $GROUPS_COUNT" >> $LOG_FILE
echo "  - Файлов расписания: $SCHEDULE_COUNT" >> $LOG_FILE
echo "  - Скопировано в frontend: $FRONTEND_SCHEDULE_COUNT" >> $LOG_FILE

echo "✅ Обновление завершено успешно!"
echo "✅ Обновление завершено успешно!" >> $LOG_FILE
echo "📅 Время завершения: $(date '+%Y-%m-%d %H:%M:%S')"
echo "📅 Время завершения: $(date '+%Y-%m-%d %H:%M:%S')" >> $LOG_FILE
echo "" >> $LOG_FILE
