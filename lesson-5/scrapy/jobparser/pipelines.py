# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import re


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacansy_305

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item


class SalaryPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'hhru':
            currencies = {'EUR': 84.31, 'USD': 78.24, 'KZT': 0.17, 'руб': 1, 'грн': 2.81, 'сум': 0.0082}
            item['salary_min'] = 0
            item['salary_max'] = 0
            if 'з/п не указана' not in item['salary'] and ' з/п не указана' not in item[
                'salary']:
                item['salary'] = ' '.join(item['salary'])
                currency = re.findall(r'([a-яА-ЯёЁA-Za-z]{3})', str(item['salary']))[0]
                currency_rate = currencies[currency]
                if 'от' in item['salary'] and 'до' in item['salary'].replace('до вычета налогов', ''):
                    item['salary_min'] = int(int(re.sub(r'\D', '', item['salary'].split('до')[0])) * currency_rate)
                    item['salary_max'] = int(int(re.sub(r'\D', '', item['salary'].split('до')[1])) * currency_rate)
                elif 'от' in item['salary']:
                    item['salary_min'] = int(int(re.sub(r'\D', '', item['salary'])) * currency_rate)
                elif 'до' in item['salary']:
                    item['salary_max'] = int(int(re.sub(r'\D', '', item['salary'])) * currency_rate)
        elif spider.name == 'SJru':
            item['salary'] = ' '.join(item['salary'])
            if 'от' in item['salary']:
                item['salary_min'] = re.sub(r'\D', '', item['salary']).replace('\xa0', ' ')
                item['salary_max'] = 0
            elif 'до' in item['salary'] and 'По договорённости' not in item['salary']:
                item['salary_min'] = 0
                item['salary_max'] = re.sub(r'\D', '', item['salary']).replace('\xa0', ' ')
            elif 'По договорённости' not in item['salary']:
                item['salary_min'] = re.sub(r'\D', '', item['salary'].split(' ')[0]).replace('\xa0', ' ')
                item['salary_max'] = re.sub(r'\D', '', item['salary'].split(' ')[1]).replace('\xa0', ' ')
            else:
                item['salary_min'] = 0
                item['salary_max'] = 0

        return item
