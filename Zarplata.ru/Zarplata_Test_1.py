import csv
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

driver = webdriver.Chrome('C:/Users/ALTAIR/Desktop/ParsingDodo/chromedriver-win64/chromedriver.exe')
data = []

with open('LinksForParser.txt', 'r') as file:
    base_urls = file.readlines()

for i in range(len(base_urls)):
    p = 0
    while True:
        url = f"{base_urls[i].strip()}={p}"
        print(url)  # for debug

        driver.get(url)
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        vacancies = [v.text for v in soup.find_all('a', {'class': 'vacancy-title vacancy-title_23EUM'})]
        prices = [p.text for p in soup.find_all('div', {'class': 'salary_7tPJD'})]
        links = ['https://russia.zarplata.ru' + link['href'] for link in
                 soup.find_all('a', {'class': 'vacancy-title vacancy-title_23EUM'})]
        cities = [city.find('span').text for city in soup.find_all('span', {'class': 'ui text grey'})]
        workers = [worker.find('a').text if worker.find('a') is not None else '' for worker in soup.find_all('div', {'class': 'title_7MBDL'})]

        if len(vacancies) == len(prices) == len(links) == len(cities) == len(workers):
            df = pd.DataFrame(list(zip(vacancies, prices, links, cities, workers)),
                              columns=['vacancies', 'prices', 'links', 'cities', 'workers'])

            df['dates'] = datetime.datetime.now().strftime("%d.%m.%Y")
            df.to_csv('vacancy_data.csv', mode='a', header=False, index=False, encoding='utf8')

        if not vacancies:  # If there are no more vacancies, break the loop and go to the next URL
            break

        p += 25

driver.close()