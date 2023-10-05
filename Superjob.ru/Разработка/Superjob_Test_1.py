import csv
import datetime
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd


urls = 'https://russia.superjob.ru/clients/servis-partner-yandeks-4241168.html'
driver = webdriver.Chrome('C:/Users/Эдуард/Desktop/ParsingDodo/ParsingDodo/chromedriver-win64/chromedriver.exe')
driver.get(urls)
time.sleep(5)


base_link = 'https://russia.superjob.ru'
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

products = soup.find_all('li', class_="_2Zt8G _3Xyl7 BRBDd _2Cx2b _1FtPv _1PtQU")

vacancies = []
salaries = []
links = []
cities = []
workers = []

for product in products:
    vacancy = product.find('span', class_='lBkfp zUZ9Q V5KLE N3XvH _13tC- _1tJ7H _272Qj _1DWzm')
    salary = product.find('span', class_='_2eYAG _13tC- _1tJ7H _272Qj t8vJ9')
    city = product.find('div', class_='WDWTW _2j_Dz _2676o _1uy6C _3oh01')
    worker = product.find('span', class_='_3nMqD f-test-text-vacancy-item-company-name bvvdt _1tJ7H _272Qj t8vJ9 _3s1qu')

    if vacancy and salary and city and worker:
        vacancies.append(vacancy.text if vacancy else '')
        salaries.append(salary.text if salary else '')
        cities.append(city.text if city else '')
        workers.append(worker.text if worker else '')

# новый кусок кода
for link in soup.find_all('a', class_= lambda value: value and value.startswith('_1IHWd-test-link-')):
    link_href = link.get('href')
    if "/vakansii/" in link_href:
        links.append(base_link + link_href)


if len(vacancies) == len(salaries) == len(links) == len(cities) == len(workers):
    df = pd.DataFrame(list(zip(vacancies, salaries, links, cities, workers)), columns=['Vacancies', 'Salaries', 'Links', 'Cities', 'Workers'])
    df['Date'] = datetime.datetime.now().strftime("%d.%m.%Y")
    df.to_csv('vacancy_data1.csv', mode='a', header=False, index=False, encoding='utf8')
else:
    print("All lists must have the same length.")

driver.close()