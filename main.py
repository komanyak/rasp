from get_rasp import get_schedule, json_to_ics
import os
import json
import subprocess


# subprocess.run(['python3', 'group_parser.py'])


with open('groups/groups.json', encoding='utf-8') as file:
    data = json.load(file)


if not os.path.exists("rasp"):
    os.makedirs("rasp")


count = 0
errors = 0
for inst in data["institute"]:
    for course in data["institute"][inst]:
        for category in data["institute"][inst][course]:
            for group in data["institute"][inst][course][category]:
                rasp = get_schedule(str(group))
                time.sleep(1)
                if rasp is not None:
                    try:
                        json_to_ics(rasp, "rasp/")
                        count += 1
                        print(f"\t{group}.ics\t\tSAVED\t{count}")
                    except Exception as e:
                        errors += 1
                        print(f"\t⚠️  Ошибка создания {group}.ics: {type(e).__name__}")
                else:
                    errors += 1

print(f"\n✅ Обработано: {count} групп")
if errors > 0:
    print(f"⚠️  Ошибок: {errors}")
