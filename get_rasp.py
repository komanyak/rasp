from datetime import datetime
import json
from ics import Calendar, Event
import pytz
import requests
import hashlib


def get_schedule(group):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'

    headers = {
        'User-Agent': user_agent,
    }
    # group = group.upper()
    group_hash = hashlib.md5(group.encode('utf-8')).hexdigest()
    link = "https://public.mai.ru/schedule/data/" + group_hash + ".json"

    try:
        responce = requests.get(link, headers=headers, timeout=30)
        responce.raise_for_status()
        
        if not responce.text.strip():
            return None
            
        data = json.loads(responce.text)
        return data
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"\t⚠️  Ошибка загрузки {group}: {type(e).__name__}")
        return None


def json_to_ics(data, path=""):
    calen = Calendar()

    # with open(json_file, 'r') as file:
    #     data = json.load(file)

    keys = list(data.keys())
    group = data[keys[0]]
    # print(group)
    for day in keys[1:]:
        _time = list(data[day]["pairs"].keys())

        for time in _time:
            pair = data[day]["pairs"][time]
            # print(pair)
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

            event = Event(name=pair_type + " " + pair_name, begin=formatted_begin, end=formatted_end,
                          description=lector,
                          location=room)

            calen.events.add(event)
    with open(f'{path}{group}.ics', 'w', encoding='utf-8') as f:
        f.writelines(calen.serialize_iter())

# data = get_schedule("М3О-319Бк-21")
# json_to_ics(data, "rasp/")
