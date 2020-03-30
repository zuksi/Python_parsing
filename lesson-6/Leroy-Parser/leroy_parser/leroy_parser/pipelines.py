# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import re
import os
from urllib.parse import urlparse


class LeroyParserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroy

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        meta = {'filename': item['name']}
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img,meta=meta)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None):
        return request.meta.get('filename','') + '/'+os.path.basename(urlparse(request.url).path)

class LeroyParserParameters(object):
    def process_item(self, item, spider):
        item['parameters'] = dict(zip(item['parameters_names'], item['parameters_values']))
        return item
