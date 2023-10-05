import csv
import datetime
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

url = 'https://russia.superjob.ru/vacancy/search/?keywords=Додо%20пицца'
driver = webdriver.Chrome('C:/Users/ALTAIR/Desktop/ParsingDodo/chromedriver-win64/chromedriver.exe')
driver.get(url)
time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

data = []
products = soup.find_all('div', class_="_1SROP _3K6yI")
for product in products:
    products = soup.find_all('div', class_="_1SROP _3K6yI")
    for product in products:
        f_test_search_result_items = product.find_all('div', class_='f-test-search-result-item')
        for f_test_search_result_item in f_test_search_result_items:
            vacancy_tag = product.find('span', class_='lBkfp zUZ9Q V5KLE N3XvH _13tC- _1tJ7H _272Qj _1DWzm')
            vacancy = vacancy_tag.text.strip() if vacancy_tag else None

            salary_tag = product.find('span', class_='_2eYAG _13tC- _1tJ7H _272Qj t8vJ9')
            salary = salary_tag.text.strip() if salary_tag else None

            href_tag = product.find('a', class_='_1IHWd f-test-link-Kurer_na_lichnom_avto_v_Dodo_Piccu _2_Rn8 HyxLN')
            href = 'https://russia.superjob.ru' + href_tag['href'] if href_tag else None

            city_tag = product.find('div', class_='WDWTW _2j_Dz _2676o _1uy6C _3oh01')
            city = city_tag.text.strip() if city_tag else None

            worker_tag = product.find('span', class_='_3nMqD f-test-text-vacancy-item-company-name bvvdt _1tJ7H _272Qj t8vJ9 _3s1qu')
            worker = worker_tag.text.strip() if worker_tag else None
            date = datetime.datetime.now().strftime("%d.%m.%Y")
            data.append([vacancy, salary, href, city, worker,date])

driver.close()

df = pd.DataFrame(data, columns=['Vacancy', 'Salary', 'Href_link', 'City', 'Worker','Date'])
df.to_csv('parsed_data.csv', index=False)
