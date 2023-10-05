import csv
import datetime
from concurrent.futures import ThreadPoolExecutor
import random
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

with open('C:/Users/ALTAIR/Desktop/ParsingDodo/Farpost.ru/LinksForParser.txt', 'r') as f:
    urls = f.read().splitlines()

data = []
driver = webdriver.Chrome('C:/Users/ALTAIR/Desktop/ParsingDodo/chromedriver-win64/chromedriver.exe')

for url in urls:
    driver.get(url)
    time.sleep(10)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    products = soup.find_all('tr', class_='bull-item bull-item_inline bull-item bull-item_inline')

    for vacancy in products:
        # Имя вакансии:
        vac_name_tag = vacancy.find('a', class_='bulletinLink bull-item__self-link auto-shy')
        vac_name = vac_name_tag.text if vac_name_tag else None

        # Зарплата:
        salary_tag = vacancy.find('div', class_='price-block__price')
        salary = salary_tag.text.strip() if salary_tag else None

        # Ссылка на объявление:
        href_tag = vacancy.find('a', class_='bulletinLink bull-item__self-link auto-shy')
        href = 'https://www.farpost.ru' + href_tag['href'] if href_tag else None

        # Город:
        city_tag = vacancy.find('span', class_='bull-delivery__city')
        city = city_tag.text.strip() if city_tag else None

        # Работодатель:
        worker_tag = vacancy.find('div', class_='bull-item__annotation-row')
        worker = worker_tag.text.strip() if worker_tag else None
        # Дата
        date = datetime.datetime.now().strftime("%d.%m.%Y")

        print(f"vacancy = {vac_name}")
        print(f"salary = {salary}")
        print(f"href_link = {href}")
        print(f"city = {city}")
        print(f"worker = {worker}")
        print(f"date = {date}")

        data.append([vac_name, salary, href, city, worker, date])

    # Сохраняем в CSV
    df = pd.DataFrame(data, columns=["vacancy", "salary", "href_link", "city", "worker", "date"])
    df.to_csv('C:/Users/ALTAIR/Desktop/ParsingDodo/Farpost.ru/output.csv', mode='a', header=False, index=False)
    # Очистка данных для следующего URL
    data = []

driver.quit()