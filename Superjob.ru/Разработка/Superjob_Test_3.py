import csv
import datetime
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd


url = 'https://russia.superjob.ru/vacancy/search/?keywords=KFC'
driver = webdriver.Chrome('C:/Users/Эдуард/Desktop/ParsingDodo/ParsingDodo/chromedriver-win64/chromedriver.exe')


driver.get(url)
time.sleep(5)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

vacancies = []
base_url = 'https://russia.superjob.ru'
for link in soup.find_all('a', class_= lambda value: value and value.startswith('_1IHWd f-test-link-')):
    link_href = link.get('href')
    if "/vakansii/" in link_href:
        vacancies.append(base_url + link_href)
print(vacancies)
# vacancies_data = soup.find_all('div', class_= lambda value: value and value.startswith('_'))




# for vacancy in vacancies_data:



# with open('vacancies.html', 'w', encoding='utf-8') as file:
#     for vacancy in link:
#         file.write(str(vacancy))
#         file.write("\n")
