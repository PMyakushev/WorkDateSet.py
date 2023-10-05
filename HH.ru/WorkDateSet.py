import csv
import datetime
from concurrent.futures import ThreadPoolExecutor
import random
import time
from bs4 import BeautifulSoup
from selenium import webdriver


def parse_url(page_number, url):
    time.sleep(random.randint(7, 15))

    driver = webdriver.Chrome('C:/Users/ALTAIR/Desktop/ParsingDodo/chromedriver-win64/chromedriver.exe')
    driver.get(url.format(page_number))

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    data = []

    href = soup.find('body', class_='s-friendly xs-friendly')
    if href is None:
        return data, None

    date_all = href.find_all('div', class_='serp-item')

    if not date_all:
        return data, None

    for element in date_all:
        vacancy = element.find('div', class_='vacancy-serp-item-body').find('h3', class_='bloko-header-section-3')
        if vacancy is None:
            break
        vacancy = vacancy.text
        print(vacancy)

        company = element.find('div', class_='vacancy-serp-item-body').find('div',
                                                                            class_='bloko-v-spacing-container bloko-v-spacing-container_base-2').find(
            'div', class_='bloko-text').text
        print(company)

        links = element.find('a', class_='serp-item__title').get('href')
        print(links)

        city = element.find('div', class_='vacancy-serp-item-body').find_all('div', class_="bloko-text")[1].text
        print(city)

        price_elements = element.find_all('span', class_='bloko-header-section-2')
        if price_elements:
            for price in price_elements:
                price_text = price.text.strip() if price else ""
                print(price_text)
        else:
            price_text = None
            print(price_elements)

        data.append([vacancy, company, links, city, price_text])

    driver.close()
    return data, page_number + 1


# загрузка ссылок из файла
with open('LinksForParser.txt', 'r') as file:
    urls = [line.strip() for line in file]

# Создание пула рабочих и начало парсинга
start_time = time.time()  # время перед началом парсинга
with ThreadPoolExecutor(max_workers=5) as executor:
    results = []
    for url in urls:
        data = []
        page_number = 0
        while True:  # цикл для обхода страниц
            try:
                result = executor.submit(parse_url, page_number, url).result()
                if result[0] is None or result[1] is None:
                    break
                data.extend(result[0])
                page_number = result[1]
                results.append((result[0], result[1]))
            except Exception as e:
                print(f"An error occurred while parsing: {str(e)}")
                break

            # запись данных в CSV
            with open('vacancy_data.csv', 'a', newline='', encoding='utf8') as csv_file:
                writer = csv.writer(csv_file)
                for row in result[0]:
                    writer.writerow(row + [datetime.datetime.now().strftime("%d.%m.%Y")])

data = []
for result in results:
    if result[0] is not None:
        data.extend(result[0])

end_time = time.time()  # время после парсинга
execution_time = end_time - start_time  # в секунда
