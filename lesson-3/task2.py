from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['database_1']
vacancies = db.vacancies

desired_salary = int(input('Введите сумму: '))

for vacancy in vacancies.find(
        {'$or': [{'min_salary': {'$gt': desired_salary}}, {'max_salary': {'$gt': desired_salary}}]}).sort('title'):
    pprint(vacancy)

