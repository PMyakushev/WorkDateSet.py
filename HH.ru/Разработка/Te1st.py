from bs4 import BeautifulSoup
import time
from selenium import webdriver
import csv

url_template = "https://togliatti.hh.ru/search/vacancy?utm_medium=widgetemployer&utm_campaign=hh.ru_more_link&utm_source=dev.hh.ru&utm_term=%2Fadmin%2Fwidgets%2Femployer&search_field=name&search_field=company_name&search_field=description&enable_snippets=true&L_save_area=true&employer_id=625332&page={}"

page_number = 0
data = []

while True:
    url = url_template.format(page_number)

    driver = webdriver.Chrome('C:/Users/ALTAIR/Desktop/ParsingDodo/chromedriver-win64/chromedriver.exe')
    driver.get(url)

    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    href = soup.find('body', class_='s-friendly xs-friendly')
    date_all = href.find_all('div', class_='serp-item')

    if not date_all:
        break

    for element in date_all:
        vacancy = element.find('div', class_='vacancy-serp-item-body').find('h3', class_ = 'bloko-header-section-3')
        if vacancy is None:
            break
        vacancy = vacancy.text
        vacancy = element.find('div', class_='vacancy-serp-item-body').find('h3', class_='bloko-header-section-3').text
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
    page_number += 1

with open('vacancy_data.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Vacancy', 'Company', 'Link', 'City', 'Price'])
    writer.writerows(data)