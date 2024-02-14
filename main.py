from get_rasp import get_schedule, json_to_ics
import os
import json
import subprocess


subprocess.run(['python', 'group_parser.py'])


with open('groups/groups.json', encoding='utf-8') as file:
    data = json.load(file)


if not os.path.exists("rasp"):
    os.makedirs("rasp")


count = 0
for inst in data["institute"]:
    for course in data["institute"][inst]:
        for category in data["institute"][inst][course]:
            for group in data["institute"][inst][course][category]:
                rasp = get_schedule(str(group))
                json_to_ics(rasp, "rasp/")
                count += 1
                print(f"\t{group}.ics\t\tSAVED\t{count}")
