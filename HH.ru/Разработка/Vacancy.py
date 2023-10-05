import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import time
import re
import csv
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
}


data = []
for p in range(0, 12):
    url = f'https://togliatti.hh.ru/search/vacancy?utm_medium=widgetemployer&utm_campaign=hh.ru_more_link&utm_source=dev.hh.ru&utm_term=%2Fadmin%2Fwidgets%2Femployer&search_field=name&search_field=company_name&search_field=description&enable_snippets=true&employer_id=625332&only_with_salary=true&L_save_area=true&page={p}'
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.text, 'lxml')
    time.sleep(10)

    href = soup.find('body', class_='s-friendly xs-friendly')
    date_all = href.find_all('div', class_='serp-item')

    for element in date_all:
        vacancy = element.find('div', class_='vacancy-serp-item-body').find('h3', class_ = 'bloko-header-section-3')
        company = element.find('div', class_='vacancy-serp-item-body').find('div', class_ = 'bloko-v-spacing-container bloko-v-spacing-container_base-2').find('div', class_ = 'bloko-text').text
        links = element.find('a', class_='serp-item__title').get('href')
        city = element.find('div', class_='vacancy-serp-item-body').find_all('div', class_= "bloko-text")[1].text

        price_elements = element.find_all('span', class_='bloko-header-section-2')
        if price_elements:
            for price in price_elements:
                price_text = price.text.strip() if price else ""
                print(price_text)
        else:
            price_text = None
            # print(price_elements)
        data.append([vacancy.text, company, links, city, price_text])

# Записать данные в файл CSV
with open('vacancy_data.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Vacancy', 'Company', 'Link', 'City', 'Price'])
    writer.writerows(data)






# for hrefs in href:
#     links = hrefs.find('div', class_ ='serp-item')
#     print(links)

# with open('file.html', 'w', encoding='utf-8') as file:
#     file.write(str(vacancy))
