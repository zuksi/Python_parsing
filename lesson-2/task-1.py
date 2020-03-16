from bs4 import BeautifulSoup as bs
import requests

import pandas as pd
from pprint import pprint
from selenium import webdriver
import re

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/Users/Laptop/AppData/Local/Temp/Rar$EXa11764.15849/chromedriver", options=options)


def get_parsed_page(main_link, second_link):
    new_link = main_link + second_link
    driver.get(new_link)
    source = driver.page_source
    parsed_page = bs(source, 'lxml')
    return parsed_page


def get_product_data(category, subcategory, name, features, score, link):
    product_data = {}
    product_data['name'] = name
    product_data['category'] = category
    product_data['subcategory'] = subcategory
    safety = 0
    quality = 0
    for feature in features:
        if 'Безопасность' in feature.getText():
            safety = re.findall(r'\d+[/.]?\d+',feature.getText())
        elif 'Качество' in feature.getText():
            quality = re.findall(r'\d+[/.]?\d+',feature.getText())
    product_data['quality'] = quality
    product_data['safety'] = safety
    product_data['score'] = score
    product_data['site'] = link

    return product_data


products = []
main_link1 = 'https://rskrf.ru'
parsed_general = get_parsed_page(main_link1, '/ratings/produkty-pitaniya/')

categories = parsed_general.find('div', {'class': 'categories'}).findChildren(recursive=False)

for category in categories:
    cat_link = category.find('a')['href']
    category_page = get_parsed_page(main_link1, cat_link)

    subcategories = category_page.find('div', {'class': 'categories'}).findChildren(recursive=False)

    for subcategory in subcategories:
        subcat_link = subcategory.find('a')['href']
        subcategory_page = get_parsed_page(main_link1, subcat_link)

        next_but = subcategory_page.find('div', {'class': 'col-xl-12 col-12 more-goods-container'})
        parsed_ratings = subcategory_page
        i = 13
        while next_but is not None:
            next_page = driver.find_elements_by_class_name('btn')[i]
            driver.execute_script("arguments[0].click();", next_page)
            new_page = driver.page_source
            parsed_ratings = bs(new_page, 'lxml')
            next_but = parsed_ratings.find('div', {'class': 'col-xl-12 col-12 more-goods-container'})
            i += 12

        category = parsed_ratings.find_all('span', {'itemprop': 'name'})[3].getText()
        subcategory = parsed_ratings.find('h1', {'itemprop': 'name'}).getText()

        products_block = parsed_ratings.find('div', {'class': 'product-row row rating-id'})
        products_list = products_block.findChildren(recursive=False)
        for product in products_list:
            product_data = {}
            if product is not None:
                product_name = product.find('h5', {
                    'class': ['card-title with-text', 'card-title with-text with-price', 'card-title with-price',
                              'card-title']}).getText().replace('\n                                   ', '')
                prod_features = product.find_all('div', {'class': 'feature-item'})
                score = product.find('div',
                                     {
                                         'class': 'starrating readonly d-inline-flex flex-row-reverse float-left'}).getText()

                link = main_link1 + subcat_link
                product_data = get_product_data(category, subcategory, product_name, prod_features, score,
                                                link)
                print(product_data)
                products.append(product_data)


main_link2 = 'https://roscontrol.com'
rating_link = '/category/produkti'

start_page = get_parsed_page(main_link2, rating_link)

categories2 = start_page.find('div', {'class': 'grid-row grid-flex-mobile'}).findChildren(recursive=False)

for category in categories2:
    cat_link = category.find('a')['href']
    category_page = get_parsed_page(main_link2, cat_link)

    subcat = category_page.find('div', {'class': 'grid-row grid-flex-mobile'})
    if subcat is not None:
        subcategories2 = subcat.findChildren(recursive=False)
        for subcategory in subcategories2:
            subcat_link = subcategory.find('a')['href']
            subcategory_page = get_parsed_page(main_link2, subcat_link)
            pages_num = subcategory_page.find('div', {'class': 'page-pagination'})
            if pages_num is not None:
                pages = []
                pages_list = pages_num.findChildren(recursive=False)

                for page in pages_list:
                    if page['href'] not in pages:
                        page_link = main_link2 + page['href']
                        products_page = get_parsed_page(main_link2, page['href'])
                        products_block = products_page.find_all('div', {'class': 'grid-row'})[5]
                        products_list = products_block.findChildren(recursive=False)
                        for product in products_list:
                            category = products_page.find_all('span', {'itemprop': 'name'})[1].getText()
                            subcategory = products_page.find('h1', {
                                'class': 'main-title util-inline-block main-title-with-social'}).getText().replace(
                                ' - рейтинг', '')
                            product_name = product.find('div', {'class': 'product__item-link'}).getText()
                            prod_features = product.find_all('div', {'class': 'row'})
                            score = product.find('div', {
                                'class': ['rate green rating-value', 'rate violation-value', 'rate blacklist-value',
                                          'rate wait-value not-tested-m', 'rate wait-value']}).getText()

                            product_data = get_product_data(category, subcategory, product_name, prod_features, score,
                                                            page_link)

                            products.append(product_data)
                        pages.append(page['href'])

            else:
                products_block = subcategory_page.find('div', {'class': 'grid-row'})
                products_list = products_block.findChildren(recursive=False)
                for product in products_list:
                    category = subcategory_page.find_all('span', {'itemprop': 'name'})[1].getText()
                    subcategory = subcategory_page.find('h1', {
                        'class': 'main-title util-inline-block main-title-with-social'}).getText().replace(
                        ' - рейтинг', '')
                    product_name = product.find('div', {'class': 'product__item-link'}).getText()
                    prod_features = product.find_all('div', {'class': 'row'})
                    score = product.find('div', {
                        'class': ['rate green rating-value', 'rate violation-value', 'rate blacklist-value',
                                  'rate wait-value not-tested-m', 'rate wait-value']}).getText()
                    product_data = get_product_data(category, subcategory, product_name, prod_features, score,
                                                    subcat_link)
                    products.append(product_data)

    else:
        pages_num = category_page.find('div', {'class': 'page-pagination'})
        if pages_num is not None:
            pages = []
            pages_list = pages_num.findChildren(recursive=False)

            for page in pages_list:
                if page['href'] not in pages:
                    page_link = main_link2 + page['href']
                    products_page = get_parsed_page(page_link)
                    products_block = products_page.find('div', {'class': 'grid-row'})
                    products_list = products_block.findChildren(recursive=False)

                    for product in products_list:
                        category = products_page.find_all('span', {'itemprop': 'name'})[1].getText()
                        subcategory = products_page.find('h1', {
                            'class': 'main-title util-inline-block main-title-with-social'}).getText().replace(
                            ' - рейтинг', '')
                        product_name = product.find('div', {'class': 'product__item-link'}).getText()
                        prod_features = product.find_all('div', {'class': 'row'})
                        score = product.find('div', {
                            'class': ['rate green rating-value', 'rate violation-value', 'rate blacklist-value',
                                      'rate wait-value not-tested-m', 'rate wait-value']}).getText()
                        product_data = get_product_data(category, subcategory, product_name, prod_features, score,
                                                        page_link)
                        products.append(product_data)
                    pages.append(page['href'])

        else:
            products_block = category_page.find('div', {'class': 'grid-row'})
            products_list = products_block.findChildren(recursive=False)
            for product in products_list:
                category = category_page.find_all('span', {'itemprop': 'name'})[1].getText()
                subcategory = category_page.find('h1', {
                    'class': 'main-title util-inline-block main-title-with-social'}).getText().replace(
                    ' - рейтинг', '')
                product_name = product.find('div', {'class': 'product__item-link'}).getText()
                prod_features = product.find_all('div', {'class': 'row'})
                score = product.find('div', {
                    'class': ['rate green rating-value', 'rate violation-value', 'rate blacklist-value',
                              'rate wait-value not-tested-m', 'rate wait-value']}).getText()
                product_data = get_product_data(category, subcategory, product_name, prod_features, score,
                                                cat_link)
                products.append(product_data)

products_rating = pd.DataFrame(products,
                               columns=['name', 'category', 'subcategory', 'safety', 'quality', 'score', 'site'])

print(products_rating)
