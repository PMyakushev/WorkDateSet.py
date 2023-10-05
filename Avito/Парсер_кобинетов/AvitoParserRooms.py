from bs4 import BeautifulSoup
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
import random
import time
import csv
import datetime

start_time = datetime.datetime.now()


def parse_page(driver):
    time.sleep(random.randint(5, 15))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    company = soup.find('h4',class_='styles-module-root-TWVKW styles-module-root-_KFFt styles-module-size_xl-bDks4 styles-module-size_xl_dense-tj0C4 styles-module-size_xl-_yeyd styles-module-size_dense-z56yO styles-module-weight_bold-Kpd5F stylesMarningNormal-module-root-OSCNq stylesMarningNormal-module-header-xl-rJXpZ').text
    items = soup.find_all("div", class_="iva-item-root-_lk9K")

    try:
        current_time = datetime.datetime.now().strftime("%d.%m.%Y")
    except Exception as e:
        print(f"Error occurred when trying to get the current date & time: {e}")

    data = []
    for item in items:
        link = 'https://www.avito.ru' + \
               item.find('a', class_="styles-module-root-QmppR styles-module-root_noVisited-aFA10")['href']
        vacancy = item.find('h3', class_="styles-module-root-TWVKW").text
        location = item.find('div', class_="geo-root-zPwRk").text.strip()
        price = item.find('strong', class_="styles-module-root-LIAav").text
        data.append([company,link, price, vacancy, location, current_time])  # add current_time

    # print(f"Gathered data for this page: {data}")
    return data


def parse_url(url):
    driver = webdriver.Chrome('C:/Users/ALTAIR/Desktop/ParsingDodo/Avito/chromedriver-win64/chromedriver.exe')   # be sure to edit this line with your own path to chromedriver
    data = []
    driver.get(url)
    print(f"Scanning URL: {url}")
    page_data = parse_page(driver)  # Получаем данные страницы, вызывая функцию parse_page
    if page_data:
        data.extend(page_data)
    driver.quit()
    # print(f"Total data for this URL: {data}")
    return data



with ThreadPoolExecutor(max_workers=5) as executor:
    with open('LinksForParser_rooms.txt', 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    for url in urls:
        result = executor.submit(parse_url, url).result()
        with open('vacancy_data_avito_rooms.csv', 'a', newline='', encoding='utf8') as csv_file:
            writer = csv.writer(csv_file)
            for row in result:
                writer.writerow(row)  # now we can just write the row as is because we've already added the date
# print(f"Final result: {result}")
end_time = datetime.datetime.now()
print(f"Runtime: {end_time - start_time}")