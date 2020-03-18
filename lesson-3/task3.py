from pymongo import MongoClient
from pprint import pprint
import lxml as lxml
from bs4 import BeautifulSoup as bs
import requests
import re
import json

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

client = MongoClient('localhost', 27017)
db = client['database_1']
vacancies = db.vacancies

main_link = 'https://hh.ru'
query = '+'.join(input('Введите название вакансии: ').split())
new_link = main_link + '/search/vacancy?area=113&st=searchVacancy&text=' + query
html = requests.get(new_link, headers=header).text
parsed_html = bs(html, 'lxml')

pages_list = parsed_html.find('div', {'data-qa': 'pager-block'}).findChildren(recursive=False)
pages_num = pages_list[-3].find('a', {'class': 'bloko-button HH-Pager-Control'}).getText()

for i in range(int(pages_num)):
    page_link = new_link + '&page=' + str(i)
    page_source = requests.get(page_link, headers=header).text
    page = bs(page_source, 'lxml')

    vacancies_block = page.find('div', {'class': 'vacancy-serp'})
    vacancies_list = vacancies_block.findChildren(recursive=False)

    for vacancy in vacancies_list:
        vacancy_data = {}
        vacancy_info = vacancy.find('div', {'class': 'vacancy-serp-item__info'})
        if vacancy_info is not None:
            vacancy_title = vacancy_info.getText()
            employer = vacancy.find('div', {'class': 'vacancy-serp-item__meta-info'}).getText().replace('\xa0', '')
            city = vacancy.find_all('div', {'class': 'vacancy-serp-item__meta-info'})[1].getText().split(',')[0]
            salary_block = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'})
            if salary_block is not None:
                salary = salary_block.getText()
                currency = salary[-4:]
                currency_rate = 1 if currency == 'руб.' else 82.47
                if 'от' in salary:
                    min_salary = '-'
                    max_salary = int(re.sub(r'\D', '', salary)) * currency_rate
                elif 'до' in salary:
                    min_salary = int(re.sub(r'\D', '', salary)) * currency_rate
                    max_salary = '-'
                elif '-' in salary:
                    min_salary = int(re.sub(r'\D', '', salary.split('-')[0])) * currency_rate
                    max_salary = int(re.sub(r'\D', '', salary.split('-')[1])) * currency_rate
                else:
                    min_salary = '-'
                    max_salary = '-'
                link = vacancy.find('a')['href']
                site = page_link

                vacancy_data['title'] = vacancy_title
                vacancy_data['employer'] = employer
                vacancy_data['city'] = city
                vacancy_data['min_salary'] = min_salary
                vacancy_data['max_salary'] = max_salary
                vacancy_data['link'] = link
                vacancy_data['site'] = site

                if vacancies.count_documents({'$and':[{'title': vacancy_title}, {'employer': employer}, {'city': city},
                         {'min_salary': min_salary}, {'max_salary': max_salary}]}) == 0:
                    vacancies.insert_one(vacancy_data)

main_link2 = 'https://russia.superjob.ru'
query2 = '+'.join(input('Введите название вакансии: ').split())
new_link2 = main_link2 + '/vacancy/search/?keywords=' + query2
html2 = requests.get(new_link2, headers=header).text
parsed_html2 = bs(html2, 'lxml')

pages_list2 = parsed_html2.find('div', {'class': 'L1p51'}).findChildren(recursive=False)
pages_num2 = pages_list2[-2].getText()

for i in range(1, int(pages_num2) + 1):
    page_link = new_link2 + '&page=' + str(i)
    page_source = requests.get(page_link, headers=header).text
    page = bs(page_source, 'lxml')

    vacancies_block = page.find('div', {'style': 'display: block'})
    vacancies_list = page.find_all('div', {'class': '_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr'})

    for vacancy in vacancies_list:
        vacancy_data = {}
        vacancy_info = vacancy.find_all('div', {'class': '_2g1F-'})[3]
        vacancy_title = vacancy_info.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'})
        if vacancy_title is not None:
            title = vacancy_title.getText()
            employer = vacancy.find_all('div', {'class': '_2g1F-'})[6].getText()
            city = vacancy.find_all('div', {'class': '_2g1F-'})[7].getText().split(' • ')[1]
            salary_block = vacancy.find_all('div', {'class': '_2g1F-'})[8]
            if salary_block is not None:
                salary = salary_block.getText()
                currency = salary[-2:]
                if 'от' in salary:
                    min_salary = '-'
                    max_salary = re.sub(r'\D', '', salary).replace('\xa0', ' ')
                elif 'до' in salary and 'По договорённости' not in salary:
                    min_salary = re.sub(r'\D', '', salary).replace('\xa0', ' ')
                    max_salary = '-'
                elif '—' in salary:
                    min_salary = re.sub(r'\D', '', salary.split('—')[0]).replace('\xa0', ' ')
                    max_salary = re.sub(r'\D', '', salary.split('—')[1]).replace('\xa0', ' ')
                else:
                    min_salary = '-'
                    max_salary = '-'
                link = main_link2 + vacancy.find_all('div', {'class': '_2g1F-'})[4].find('a')['href']
                site = page_link

                vacancy_data['title'] = title
                vacancy_data['employer'] = employer
                vacancy_data['city'] = city
                vacancy_data['min_salary'] = min_salary
                vacancy_data['max_salary'] = max_salary
                vacancy_data['link'] = link
                vacancy_data['site'] = site

                if vacancies.count_documents({'$and':[{'title': title}, {'employer': employer}, {'city': city},
                         {'min_salary': min_salary}, {'max_salary': max_salary}]}) == 0:
                    vacancies.insert_one(vacancy_data)
