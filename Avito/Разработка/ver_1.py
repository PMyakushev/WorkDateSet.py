import time
import csv
import random
import datetime
from bs4 import BeautifulSoup
from rotating_proxy.rotating_proxy import RotatingProxy
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor

start_time = datetime.datetime.now()

def parse_page(driver):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    data = []

    vacancies = soup.find_all('div', class_='iva-item-root-_lk9K')

    for vacancy in vacancies:
        try:
            job_title = vacancy.find('h3', itemprop='name').text
            salary = vacancy.find('span', class_='_1OuF__xQ4').text
            partial_link = vacancy.find('a', itemprop='url')['href']
            full_link = 'https://www.avito.ru' + partial_link
            city = vacancy.find('div', class_='geo-root-zPwRk').find('p').get_text()

            data.append([job_title, salary, full_link, city])
        except AttributeError:
            continue
    return data

def parse_url(url):
    proxy = RotatingProxy()   # Initialize rotating proxy. You retrieve a new proxy by using proxy.get()
    PROXY = proxy.get()

    webdriver.DesiredCapabilities.CHROME['proxy']={
        "httpProxy":PROXY,
        "ftpProxy":PROXY,
        "sslProxy":PROXY,
        "noProxy":None,
        "proxyType":"MANUAL",
        "autodetect":False
    }

    driver = webdriver.Chrome('path_to_your_chromedriver', desired_capabilities=webdriver.DesiredCapabilities.CHROME)

    data = []
    page_number = 1

    while True:
        driver.get(f'{url}&p={page_number}')
        time.sleep(5)

        page_data = parse_page(driver)
        if page_data:
            data.extend(page_data)
            page_number += 1
            proxy.rotate()  # Rotate to a new proxy
        else:
            break

    driver.quit()
    return data

with open('LinksForParser.txt', 'r') as file:
    urls = [line.strip() for line in file.readlines()]

data = []

with ThreadPoolExecutor(max_workers=5) as executor:
    for url in urls:
        data.extend(executor.submit(parse_url, url).result())

with open('vacancy_data_avito.csv', 'w', newline='', encoding='utf8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Job Title", "Salary", "Link", "City", "Scrape Time"])
    for row in data:
        writer.writerow(row + [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

end_time = datetime.datetime.now()
print(f"Время выполнения: {end_time - start_time}")