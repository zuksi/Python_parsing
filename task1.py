# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json

username = input("Введите имя пользователя на github:")


main_link = 'https://api.github.com/users'

response = requests.get(f'{main_link}/{username}/repos')
data = json.loads(response.text)

repo_names = {}

for i in data:
    repo_names[data.index(i)] = i['name']

print(repo_names)

with open("repos.json", "w") as f:
    json.dump(repo_names,f)

