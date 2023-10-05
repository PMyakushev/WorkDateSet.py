import csv
import datetime
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

data = []

with open('LinksForParser.txt', 'r') as f:
    urls = [line.strip() for line in f.readlines()]

for url in urls:
    driver = webdriver.Chrome('C:/Users/ALTAIR/Desktop/ParsingDodo/chromedriver-win64/chromedriver.exe')
    driver.get(url)
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    products = soup.find_all('li', class_="_2Zt8G _3Xyl7 BRBDd _2Cx2b _1FtPv _1PtQU")
    links = soup.find_all('span', class_='lBkfp zUZ9Q V5KLE N3XvH _13tC- _1tJ7H _272Qj _1DWzm')

    for product in products:
        vacancy = product.find('span', class_='lBkfp zUZ9Q V5KLE N3XvH _13tC- _1tJ7H _272Qj _1DWzm').text
        for link in links:
            href_link = 'https://russia.superjob.ru'+link.find('a').get('href')
        salary = product.find('span', class_='_2eYAG _13tC- _1tJ7H _272Qj t8vJ9').text
        city = product.find('div', class_='WDWTW _2j_Dz _2676o _1uy6C _3oh01').text
        worker = product.find('span', class_='_3nMqD f-test-text-vacancy-item-company-name bvvdt _1tJ7H _272Qj t8vJ9 _3s1qu').text

        data.append({
            'Vacancy': vacancy,
            'Salary': salary,
            'Href': href_link,
            'City': city,
            'Worker': worker,
            'Date': datetime.datetime.now().strftime("%d.%m.%Y")
        })
        df = pd.DataFrame(data)
        df.to_csv('parsed_data.csv', mode='a', index=False)
        data = []

driver.quit()
