import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from concurrent.futures import ThreadPoolExecutor
import time
import csv
import datetime

start_time = datetime.datetime.now()

PROXY_LIST = ['https://178.140.177.145:8889']  # замените на список ваших прокси

def parse_page(driver):
    time.sleep(random.randint(30, 50))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    data = []
    vacancies = soup.find_all('div', class_='iva-item-root-_jk9K')
    for vacancy in vacancies:
        job_title = vacancy.find('h3', itemprop='name').text
        if job_title:
            salary = vacancy.find('p', class_='styles-module-root-_KFFt').find_all('strong')[0].text
            partial_link = vacancy.find('a', itemprop='url')['href']
            full_link = 'https://www.avito.ru' + partial_link
            city = vacancy.find('div', class_='geo-root-zPwRk').find('p').get_text()
            data.append([job_title, salary, full_link, city])
    return data

def parse_url(url):
    proxy_to_apply = random.choice(PROXY_LIST)
    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": proxy_to_apply,
        "ftpProxy": proxy_to_apply,
        "sslProxy": proxy_to_apply,
        "proxyType": "MANUAL",
    }
    driver = webdriver.Chrome('C:/Users/ALTAIR/Desktop/ParsingDodo/Avito/chromedriver-win64/chromedriver.exe')
    data = []
    page_number = 1
    while True:
        driver.get(f'{url}&p={page_number}')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        page_data = parse_page(driver)
        if page_data:
            data.extend(page_data)
            page_number += 1
        else:
            break
    driver.quit()
    return data

with open('vacancy_data_avito1.csv', 'w', newline='', encoding='utf8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Job Title", "Salary", "Link", "City", "Scrape Time"])
    # в вашем коде нет чтения ссылок из файла, добавим этот код
    with open('Парсер общего поиска/LinksForParser.txt', 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    with ThreadPoolExecutor(max_workers=5) as executor:
        for url in urls:
            result = executor.submit(parse_url, url).result()
            for row in result:
                writer.writerow(row + [datetime.datetime.now().strftime("%d.%m.%Y")])

end_time = datetime.datetime.now()
print(f"Runtime: {end_time - start_time}")