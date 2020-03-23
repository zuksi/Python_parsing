import requests
from pprint import pprint
from lxml import html
import re
import json

news_collection = []

main_link = 'https://news.mail.ru'
response = requests.get(main_link).text
tree = html.fromstring(response)

news_list = tree.xpath("//div[@data-counter-id='20268335']")

for news in news_list:

    title = news.xpath(
        ".//span[@class='photo__title photo__title_new photo__title_new_hidden js-topnews__notification']/text() | .//a[@class='list__text']/text() ")
    link = news.xpath(".//a/@href")
    source = []
    date = []
    for l in link:
        news_link = requests.get(main_link + l).text
        l_tree = html.fromstring(news_link)
        l_source = l_tree.xpath(".//a[@class='link color_gray breadcrumbs__link']/span/text()")
        l_date = l_tree.xpath(".//span[@class='note__text breadcrumbs__text js-ago']/text()")

        source.append(l_source)
        date.append(l_date)

    news_data = zip(title, link, source, date)
    for title, link, source, date in news_data:
        news_info = {}
        news_info['title'] = title.replace('\xa0',' ')
        news_info['link'] = main_link + link
        news_info['source'] = source[0]
        news_info['date'] = date[0]

        print(news_info)
        news_collection.append(news_info)


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
lenta_link = 'https://lenta.ru'
lenta_response = requests.get(lenta_link, headers=header).text
lenta_tree = html.fromstring(lenta_response)

news_lenta = lenta_tree.xpath("//div[contains(@class,'span4')]")

for news in news_lenta:
    news_info = {}
    title = news.xpath(".//h2/a/text() | .//div[contains(@class,'item')]/a/text() ")
    link = news.xpath(".//div[contains(@class,'item')]/a/@href")
    date = news.xpath(".//a/time/text()")

    news_data = zip(title, link, date)
    for title, link, date in news_data:
        news_info = {}
        news_info['title'] = title.replace('\xa0',' ')
        news_info['link'] = lenta_link + link
        news_info['source'] = 'Lenta.ru'
        news_info['date'] = date

        news_collection.append(news_info)


yandex_link = 'https://yandex.ru/news'
yandex_response = requests.get(yandex_link, headers=header).text
yandex_tree = html.fromstring(yandex_response)

news_yandex = yandex_tree.xpath("(//div[contains(@class,'set stories')])[position() <4]")

for news in news_yandex:
    news_info = {}
    title = news.xpath(".//h2[@class='story__title']/a/text() ")
    link = news.xpath(".//h2[@class='story__title']/a/@href ")
    date_source = news.xpath(".//div[@class='story__date']/text()")

    news_data = zip(title, link, date_source)
    for title, link, date_source in news_data:
        news_info = {}
        news_info['title'] = title.replace('\xa0',' ')
        news_info['link'] = 'https://yandex.ru' + link
        news_info['source'] = re.sub('\d\d:\d\d', '', date_source.replace(' вчера\xa0в\xa0', ''))
        news_info['date'] = 'вчера в ' + str(
            re.findall('\d\d:\d\d', date_source)[0]) if 'вчера' in str(date_source) else str(
            re.findall('\d\d:\d\d', date_source)[0])

        news_collection.append(news_info)

print(news_collection)

with open("news.json", "w") as f:
    json.dump(news_collection,f)

