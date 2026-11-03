from get_rasp import get_schedule, json_to_ics
import os
import json
import subprocess


# subprocess.run(['python3', 'group_parser.py'])


with open('groups/groups.json', encoding='utf-8') as file:
    data = json.load(file)


if not os.path.exists("rasp"):
    os.makedirs("rasp")


success_count = 0
updated_count = 0
unchanged_count = 0
error_count = 0
total_count = 0

for inst in data["institute"]:
    for course in data["institute"][inst]:
        for category in data["institute"][inst][course]:
            for group in data["institute"][inst][course][category]:
                total_count += 1
                rasp = get_schedule(str(group))
                if rasp is not None:
                    try:
                        was_updated = json_to_ics(rasp, "rasp/")
                        success_count += 1
                        if was_updated:
                            updated_count += 1
                            print(f"\t✅ {group}.ics\t\tUPDATED\t[{success_count}/{total_count}]")
                        else:
                            unchanged_count += 1
                            print(f"\t➖ {group}.ics\t\tUNCHANGED\t[{success_count}/{total_count}]")
                    except Exception as e:
                        error_count += 1
                        print(f"\t⚠️  Ошибка создания {group}.ics: {type(e).__name__}")
                else:
                    error_count += 1

print("\n" + "="*50)
print("📊 СТАТИСТИКА ОБНОВЛЕНИЯ РАСПИСАНИЙ")
print("="*50)
print(f"📚 Всего групп:              {total_count}")
print(f"✅ Успешно обработано:       {success_count} ({success_count*100//total_count if total_count > 0 else 0}%)")
print(f"   ├─ 🔄 Обновлено:          {updated_count}")
print(f"   └─ ➖ Без изменений:       {unchanged_count}")
print(f"❌ Не удалось получить:      {error_count} ({error_count*100//total_count if total_count > 0 else 0}%)")
print("="*50)

if total_count and success_count == 0:
    raise SystemExit("Не удалось получить расписание ни для одной группы")
