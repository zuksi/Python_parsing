# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import json

user = 'PsyXe'
key = 'YD8tDfqXEIZYotnXDH3mMHg2tGr56NIIf9DrxVNualj8Tf23'

params = {
    'user-id': user,
    'api-key': key,
    'output-format': 'json',
    'content':'Mike is a douchebag and his sister is a whore'
}

req = requests.get('https://neutrinoapi.net/bad-word-filter', params=params)

response_bad_words = req.text
print('Ответ: \n', response_bad_words)

params2 = {
    'user-id': user,
    'api-key': key,
    'output-format': 'json',
    'address':'Moulin Rouge',
    'language-code': 'ru'
}

req2 = requests.get('https://neutrinoapi.net/geocode-address', params=params2)

response_geo = req2.text
print('Ответ: \n', response_geo)

params3 = {
    'user-id': user,
    'api-key': key,
    'output-format': 'json',
    'email':'LizaMinelli@gmail.com'
}

req3 = requests.get('https://neutrinoapi.net/email-verify', params=params3)

response_email = req3.text
print('Ответ: \n', response_email)


with open("neutrino.json", "w") as f:
    json.dump(response_bad_words,f)
    json.dump(response_geo, f)
    json.dump(response_email, f)




