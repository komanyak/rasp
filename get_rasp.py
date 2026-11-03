from datetime import datetime
import json
from ics import Calendar, Event
import pytz
import requests
import hashlib
import os
import time
import warnings
from urllib.parse import urlparse

from urllib3.exceptions import InsecureRequestWarning


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

TLS_VERIFICATION_FAILED_HOSTS = set()
MIN_REQUEST_INTERVAL_SECONDS = 0.5
MAX_TRANSIENT_RETRIES = 4
RETRYABLE_STATUS_CODES = {403, 429, 500, 502, 503, 504}
last_request_at = 0.0


class ScheduleServiceBlocked(RuntimeError):
    """The schedule API rejected a whole batch, usually due to rate limiting."""


def request_with_rate_limit(url, headers, timeout, verify=True):
    """Keep the request rate below MAI's anti-bot threshold."""
    global last_request_at

    wait_seconds = MIN_REQUEST_INTERVAL_SECONDS - (time.monotonic() - last_request_at)
    if wait_seconds > 0:
        time.sleep(wait_seconds)

    response = requests.get(url, headers=headers, timeout=timeout, verify=verify)
    last_request_at = time.monotonic()
    return response


def get_mai_response(url, headers, timeout):
    """Request a MAI endpoint, falling back only for its invalid TLS chain."""
    host = urlparse(url).hostname

    if host in TLS_VERIFICATION_FAILED_HOSTS:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", InsecureRequestWarning)
            return request_with_rate_limit(url, headers, timeout, verify=False)

    try:
        return request_with_rate_limit(url, headers, timeout)
    except requests.exceptions.SSLError:
        TLS_VERIFICATION_FAILED_HOSTS.add(host)
        print(f"TLS verification failed for {host}; continuing with certificate verification disabled for this host.")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", InsecureRequestWarning)
            return request_with_rate_limit(url, headers, timeout, verify=False)


def get_schedule(group):
    # Use a consistent browser-like request. Rotating user agents without a
    # session makes a batch of hundreds of requests look more like a bot.
    headers = {
        'User-Agent': USER_AGENTS[0],
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://mai.ru/',
    }
    # group = group.upper()
    group_hash = hashlib.md5(group.encode('utf-8')).hexdigest()
    link = "https://public.mai.ru/schedule/data/" + group_hash + ".json"

    try:
        for attempt in range(MAX_TRANSIENT_RETRIES):
            responce = get_mai_response(link, headers, timeout=10)

            if responce.status_code not in RETRYABLE_STATUS_CODES:
                responce.raise_for_status()
                break

            if attempt == MAX_TRANSIENT_RETRIES - 1:
                if responce.status_code in {403, 429}:
                    raise ScheduleServiceBlocked(
                        f"Расписание МАИ временно недоступно: HTTP {responce.status_code}. "
                        "Прекращаем пакет, чтобы не усиливать блокировку."
                    )
                responce.raise_for_status()

            retry_after = responce.headers.get("Retry-After")
            delay_seconds = int(retry_after) if retry_after and retry_after.isdigit() else 2 ** attempt
            print(f"\t⏳ {group}: HTTP {responce.status_code}, повтор через {delay_seconds} сек.")
            time.sleep(delay_seconds)
        
        if not responce.text.strip():
            return None
            
        data = json.loads(responce.text)
        return data
    except requests.exceptions.Timeout:
        print(f"\t⏱️  Таймаут при загрузке {group} (>10 сек)")
        return None
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        status_code = getattr(e.response, "status_code", None)
        detail = f"HTTP {status_code}" if status_code else type(e).__name__
        print(f"\t⚠️  Ошибка загрузки {group}: {detail}")
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
