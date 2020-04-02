from selenium import webdriver
import ast
import json
from pymongo import MongoClient
import pprint
import time

driver = webdriver.Chrome()
driver.get('https://www.mvideo.ru/')

pages = driver.find_elements_by_class_name('carousel-paging')[2].text
products_list = []

for i in range(int(pages[-1])):
    page_button = driver.find_elements_by_class_name('carousel-paging')[2].find_elements_by_tag_name('a')[i]
    page_button.click()
    time.sleep(5)
    for j in range(4):
        product = {}
        title = driver.find_elements_by_tag_name('h4')[j].get_attribute('title')
        info =driver.find_elements_by_class_name('sel-product-tile-title')[j].get_attribute('data-product-info')
        link = driver.find_elements_by_class_name('sel-product-tile-title')[j].get_attribute('href')
        product['name'] = title
        product['price'] = float(ast.literal_eval(info)['productPriceLocal'])
        product['category'] = ast.literal_eval(info)['productCategoryName']
        product['producer'] = ast.literal_eval(info)['productVendorName']
        product['link'] = link
        products_list.append(product)

driver.close()

client = MongoClient('localhost',27017)
db = client['mvideo']
products = db.products

products.insert_many(products_list)