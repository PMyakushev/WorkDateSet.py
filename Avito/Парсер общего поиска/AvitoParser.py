from bs4 import BeautifulSoup
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
import random
import time
import csv
import datetime

start_time = datetime.datetime.now()

def parse_page(driver):
    time.sleep(random.randint(30, 50))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    data = []
    vacancies = soup.find_all('div', class_='iva-item-root-_lk9K')

    for vacancy in vacancies:
        try:
            job_title = vacancy.find('h3', itemprop='name').text
            salary =  vacancy.find('p', class_='styles-module-root-_KFFt styles-module-size_l-_oGDF styles-module-size_l_dense-Wae_G styles-module-size_l-hruVE styles-module-size_dense-z56yO stylesMarningNormal-module-root-OSCNq stylesMarningNormal-module-paragraph-l-dense-TTLmp').find_all('strong')[0].text
            partial_link = vacancy.find('a', itemprop='url')['href']
            full_link = 'https://www.avito.ru' + partial_link
            city = vacancy.find('div', class_='geo-root-zPwRk').find('p').get_text()

            data.append([job_title, salary, full_link, city])
        except AttributeError:
            continue
    return data

def solve_captcha(driver):
    while True:
        if 'captcha' in driver.current_url:
            print('Пожалуйста, решите капчу...')
            time.sleep(20)
        else:
            break

def parse_url(url):
    driver = webdriver.Chrome('C:/AvitoParser.py/chromedriver-win64/chromedriver.exe')
    data = []
    page_number = 1

    while True:
        driver.get(f'{url}&p={page_number}')
        solve_captcha(driver)
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
        writer.writerow(row + [datetime.datetime.now().strftime("%d.%m.%Y")])

end_time = datetime.datetime.now()
print(f"Время выполнения: {end_time - start_time}")