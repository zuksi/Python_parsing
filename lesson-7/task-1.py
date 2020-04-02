from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
from pymongo import MongoClient
import time

driver = webdriver.Chrome()
driver.get('https://mail.ru')

elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('study.ai_172')

domain = driver.find_element_by_name('domain')
options = domain.find_elements_by_tag_name('option')

for option in options:
    if option.text == '@mail.ru':
        option.click()

button = driver.find_elements_by_class_name('o-control')[1]
button.click()

elem = driver.find_element_by_id('mailbox:password')
elem.send_keys('NewPassword172')

elem.send_keys(Keys.RETURN)

time.sleep(10)

links = []
links_block = driver.find_elements_by_xpath("//div[@class='layout__main-frame']//a")
for link in links_block:
    links.append(link.get_attribute('href'))
    link.send_keys(Keys.ARROW_DOWN)

time.sleep(5)
new_elem = driver.find_element_by_xpath("(//div[@class='layout__main-frame']//a)[last()]")
new_elem.send_keys(Keys.DOWN)
while True:
    try:
        new_elem.send_keys(Keys.DOWN)
        new_block = driver.find_elements_by_xpath("//div[@class='layout__main-frame']//a")
        for link in new_block:
            links.append(link.get_attribute('href'))
        new_elem = driver.find_element_by_xpath("(//div[@class='layout__main-frame']//a)[last()]")
        new_elem.send_keys(Keys.DOWN)
    except Exception as e:
        break
        print('Парсинг окончен или ошибка: ', e)

letters = []
print(set(links))
for link in set(links):
    driver.get(link)
    time.sleep(10)
    letter = {}
    letter['from'] = driver.find_element_by_class_name('letter__author').find_element_by_xpath('span[1]').get_attribute('title')
    letter['date'] = driver.find_element_by_class_name('letter__date').text
    letter['subject'] = driver.find_element_by_class_name('thread__subject').text
    letter['text'] = driver.find_element_by_class_name('letter-body').text
    letters.append(letter)

driver.close()

client = MongoClient('localhost',27017)
db = client['mail']
letters = db.letters

letters.insert_many(letters)
