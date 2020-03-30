# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def price_int(value):
    value = float(value)
    return value

def parameters_cleaner(value):
    value = re.findall('(?<=[ ]{16}).+(?=[\n])', value)[0]
    is_digit = re.findall('\d', value)
    if is_digit != []:
        value = float(''.join(re.findall('[\d.]+', value)))
    return value

class LeroyParserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(price_int),output_processor=TakeFirst())
    parameters = scrapy.Field()
    parameters_names = scrapy.Field()
    parameters_values = scrapy.Field(input_processor=MapCompose(parameters_cleaner))


