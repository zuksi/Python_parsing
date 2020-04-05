import csv
from datetime import datetime
import matplotlib.pyplot as plt

f = open('C:/Users/Laptop/Downloads/opendata/opendata.csv', 'r', encoding='WINDOWS-1251')
reader = csv.DictReader(f, delimiter=',')

region = input('Введите регион: ')
name = input('Введите название показателя: ')

date_low = input('Введите начальную дату в формате yyyy-mm-dd: ')
date_upper = input('Введите конечную дату в формате yyyy-mm-dd: ')
x = []
y = []

for row in reader:
    if row['region'] == region and row['name'] == name and row['date']>= date_low and row['date']<= date_upper:
        x.append(datetime.strptime(row['date'], '%Y-%m-%d').date())
        y.append(int(row['value']))

plt.plot(x, y)

plt.show()
