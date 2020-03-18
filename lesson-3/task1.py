import json
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost',27017)
db = client['database_1']
vacancies = db.vacancies

# with open("vacancies.json", "r") as f:
#     vacancies_file = json.load(f)

# vacancies.insert_many(vacancies_file)

# for vacancy in vacancies.find():
#     pprint(vacancy)
