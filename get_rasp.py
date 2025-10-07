from datetime import datetime
import json
from ics import Calendar, Event
import pytz
import requests
import hashlib
import random
import os


# Массив различных user agents для защиты от блокировки
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'
]


def get_schedule(group):
    # Выбираем случайный user agent для каждого запроса
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
    }
    # group = group.upper()
    group_hash = hashlib.md5(group.encode('utf-8')).hexdigest()
    link = "https://public.mai.ru/schedule/data/" + group_hash + ".json"

    try:
        responce = requests.get(link, headers=headers, timeout=3)
        responce.raise_for_status()
        
        if not responce.text.strip():
            return None
            
        data = json.loads(responce.text)
        return data
    except requests.exceptions.Timeout:
        print(f"\t⏱️  Таймаут при загрузке {group} (>3 сек)")
        return None
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"\t⚠️  Ошибка загрузки {group}: {type(e).__name__}")
        return None


def json_to_ics(data, path=""):
    calen = Calendar()

    # with open(json_file, 'r') as file:
    #     data = json.load(file)

    keys = list(data.keys())
    group = data[keys[0]]
    
    # Создаем события с детерминированными UID на основе содержимого
    for day in keys[1:]:
        _time = list(data[day]["pairs"].keys())

        for time in _time:
            pair = data[day]["pairs"][time]
            pair_name = list(pair.keys())[0]
            pair_start = pair[pair_name]["time_start"]
            pair_end = pair[pair_name]["time_end"]
            lector = list(pair[pair_name]["lector"].values())[0]
            pair_type = list(pair[pair_name]["type"].keys())[0]
            room = list(pair[pair_name]["room"].values())[0]

            moscow_timezone = pytz.timezone('Europe/Moscow')

            begin_moscow = datetime.strptime(day + " " + pair_start, "%d.%m.%Y %H:%M:%S")
            end_moscow = datetime.strptime(day + " " + pair_end, "%d.%m.%Y %H:%M:%S")

            begin_utc = moscow_timezone.localize(begin_moscow).astimezone(pytz.utc)
            end_utc = moscow_timezone.localize(end_moscow).astimezone(pytz.utc)

            formatted_begin = begin_utc.strftime("%Y-%m-%d %H:%M:%S")
            formatted_end = end_utc.strftime("%Y-%m-%d %H:%M:%S")

            # Создаем детерминированный UID на основе содержимого события
            uid_string = f"{group}{day}{pair_start}{pair_name}{lector}{room}"
            uid = hashlib.md5(uid_string.encode('utf-8')).hexdigest()

            event = Event(name=pair_type + " " + pair_name, begin=formatted_begin, end=formatted_end,
                          description=lector,
                          location=room)
            event.uid = uid

            calen.events.add(event)
    
    # Генерируем новое содержимое
    new_content = ''.join(calen.serialize_iter())
    file_path = f'{path}{group}.ics'
    
    # Проверяем, нужно ли обновлять файл
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            old_content = f.read()
        
        # Сохраняем только если содержимое изменилось
        if old_content == new_content:
            return False  # Файл не изменился
    
    # Сохраняем файл
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True  # Файл был создан или обновлен

# data = get_schedule("М3О-107СВ-25")
# json_to_ics(data, "rasp/")
