from pymongo import MongoClient
from pprint import pprint
import json

client = MongoClient('localhost', 27017)
db = client['database_1']
news = db.news

with open("news.json", "r") as f:
    news_file = json.load(f)

for news in news.find():
    pprint(news)