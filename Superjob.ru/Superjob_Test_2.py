import csv
import datetime
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

def remove_duplicates(filename):
    # Reading the file using pandas
    df = pd.read_csv(filename)

    # Removing duplicates
    df = df.drop_duplicates()

    # Writing the updated data back to the file
    df.to_csv(filename, index=False)


urls = open("C:/Users/Эдуард/Desktop/ParsingDodo/ParsingDodo/Superjob.ru/LinksForParser.txt", "r", encoding='utf-8').readlines()
driver = webdriver.Chrome('C:/Users/Эдуард/Desktop/ParsingDodo/ParsingDodo/chromedriver-win64/chromedriver.exe')

for url in urls:
    driver.get(url.strip())
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    vacancies = []
    base_url = 'https://russia.superjob.ru'

    vacancies_data = soup.find_all('div', class_= lambda value: value and value.startswith('_'))

    for vacancy in vacancies_data:
        vacancy_dict = {}
        vacancy_name = vacancy.find('span', class_='_1QOlM _2OLLx _102dm _2M1jg _2IT_8 _1BJoX inakc _2EuTH')
        salary = vacancy.find('span', class_='_2eYAG _2IT_8 _1BJoX inakc GQbw5')
        link = vacancy.find('a', class_= lambda value: value and value.startswith('_1IHWd f-test-link-'))  # UPDATE HERE
        city = vacancy.find('span', class_='f-test-text-company-item-location _1nolV _1BJoX inakc _2iNjB')
        worker = vacancy.find('span', class_='_3nMqD f-test-text-vacancy-item-company-name _1jYKu _1BJoX inakc GQbw5 _30f1O')

        if vacancy_name:
            vacancy_dict["vacancy"] = vacancy_name.text
        else:
            vacancy_dict["vacancy"] = None

        if salary:
            vacancy_dict["salary"] = salary.text
        else:
            vacancy_dict["salary"] = None

        if link and "/vakansii/" in link.get('href'):
            vacancy_dict["link"] = base_url + link.get('href')
        else:
            vacancy_dict["link"] = None

        if city:
            vacancy_dict["city"] = city.text.strip()
        else:
            vacancy_dict["city"] = None

        if worker:
            vacancy_dict["worker"] = worker.text
        else:
            vacancy_dict["worker"] = None

        vacancy_dict["date"] = datetime.datetime.now().strftime("%d.%m.%Y")
        vacancies.append(vacancy_dict)

    df = pd.DataFrame(vacancies)
    df.to_csv('vacancies.csv', mode='a', index=False)  # Append data to the csv after every page

remove_duplicates('vacancies.csv')
