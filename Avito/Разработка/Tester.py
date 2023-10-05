from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from concurrent.futures import ThreadPoolExecutor
import random
import time
import csv
import datetime
from  random_proxies  import RandomProxies

rp = RandomProxies()


def random_proxy():
    return rp.random_proxy()


def get_chromedriver(user_agent=None):
    path_to_chromedriver = 'C:/AvitoParser.py/chromedriver-win64/chromedriver.exe'
    chrome_options = webdriver.ChromeOptions()

    p = Proxy()
    p.proxy_type = ProxyType.MANUAL
    p.http_proxy = user_agent
    p.ssl_proxy = user_agent

    capabilities = webdriver.DesiredCapabilities.CHROME
    p.add_to_capabilities(capabilities)

    chrome_options.add_argument('--proxy-server=%s' % user_agent)
    driver = webdriver.Chrome(path_to_chromedriver, desired_capabilities=capabilities, chrome_options=chrome_options)

    return driver


def parse_page(driver):
    time.sleep(random.randint(30, 50))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    vacancies = soup.find_all('div', class_='iva-item-root-_lk9K')

    data = []

    for vacancy in vacancies:
        try:
            job_title = vacancy('h3', itemprop='name').text
            salary = vacancy.find('p',
                                  class_='styles-module-root-_KFFt styles-module-size_l-_oGDF styles-module-size_l_dense-Wae_G styles-module-size_l-hruVE styles-module-size_dense-z56yO stylesMarningNormal-module-root-OSCNq stylesMarningNormal-module-paragraph-l-dense-TTLmp').find_all(
                'strong')[0].text
            partial_link = vacancy.find('a', itemprop='url')['href']
            full_link = 'https://www.avito.ru' + partial_link
            city = vacancy.find('div', class_='geo-root-zPwRk').find('p').get_text()

            row = [job_title, salary, full_link, city, datetime.datetime.now().strftime("%d.%m.%Y")]
            data.append(row)
        except AttributeError:
            continue

    return data


def parse_url(url):
    driver = get_chromedriver(user_agent=random_proxy())
    page_number = 1
    data = []

    while True:
        driver.get(f'{url}&p={page_number}')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        data.extend(parse_page(driver))

        page_number += 1
        time.sleep(20)

    driver.quit()
    return data


def write_to_csv(data, filename):
    with open(filename, 'a', newline='', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file)

        for row in data:
            writer.writerow(row)


start_time = datetime.datetime.now()

with open('vacancy_data_avito.csv', 'w', newline='', encoding='utf8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Job Title", "Salary", "Link", "City", "Scrape Time"])

    with ThreadPoolExecutor(max_workers=5) as executor:
        with open('LinksForParser.txt', 'r') as file:
            urls = [line.strip() for line in file.readlines()]
            for url in urls:
                data = executor.submit(parse_url, url).result()
                write_to_csv(data, 'vacancy_data_avito.csv')

end_time = datetime.datetime.now()
print(f"Runtime: {end_time - start_time}")
