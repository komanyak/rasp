from bs4 import BeautifulSoup
import requests
import json
import os




user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'

headers = {
    'User-Agent': user_agent,
}
groups = {"institute": {}}



for i in range(1, 15):

    link = f"https://mai.ru/education/studies/schedule/groups.php?department=%D0%98%D0%BD%D1%81%D1%82%D0%B8%D1%82%D1%83%D1%82+%E2%84%96{i}&course=all"

    html_doc = requests.get(link, headers=headers).text

    soup = BeautifulSoup(html_doc, 'html.parser')

    btn_group_links = soup.find_all('a', class_='btn-group')

    if (len(btn_group_links)) == 0:
        continue

    data = []

    for link in btn_group_links:
        data.append(link.text)

    data_dict = {}

    for item in data:
        _item = item.split("-")

        first_digit = _item[1][0]
        # if first_digit not in data_dict:
        #     data_dict[first_digit] = []
        # data_dict[first_digit].append(item)

        if first_digit not in data_dict:
            data_dict[first_digit] = {"bachelor": [], "magistracy": [], "postgraduate": [], "spec_high": [],
                                      "specialty": [], "basic": []}
        form = _item[1][3:]
        if form == "Бк" or form == "Б" or form == "Бки" or form == "Би":
            data_dict[first_digit]["bachelor"].append(item)

        elif form == "С" or form == "Ск":
            data_dict[first_digit]["specialty"].append(item)

        elif form == "Мк" or form == "М" or form == "Мки":
            data_dict[first_digit]["magistracy"].append(item)

        elif form == "А" or form == "Ак":
            data_dict[first_digit]["postgraduate"].append(item)

        elif form == "СВ" or form == "СВки" or form == "СВк":
            data_dict[first_digit]["spec_high"].append(item)

        elif form == "БВ" or form == "БВк":
            data_dict[first_digit]["basic"].append(item)

        else:

            print(form, _item)

    empty = []
    for course in data_dict:
        for level in data_dict[course]:
            if len(data_dict[course][level]) == 0:
                empty.append([course, level])

    for item in empty:
        del data_dict[item[0]][item[1]]

        # print(_item)

    groups["institute"][str(i)] = data_dict
    print(f"{i} Institute parsed")

if not os.path.exists("groups"):
    os.makedirs("groups")

with open(os.path.join('groups', 'groups.json'), 'w', encoding='utf-8') as json_file:
    json.dump(groups, json_file, ensure_ascii=False, indent=4)

print(f"\n\tДанные записаны в файл 'groups.json\n\n")
