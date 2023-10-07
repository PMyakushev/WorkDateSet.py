import csv
import datetime
from concurrent.futures import ThreadPoolExecutor
import random
import time
from bs4 import BeautifulSoup
from selenium import webdriver

with open('LinksPhones.txt', 'r', encoding='utf-8') as file:
    file.read()
url = 'https://togliatti.hh.ru/vacancy/68311187?from=vacancy_search_list&hhtmFrom=vacancy_search_list'
driver = webdriver.Chrome('C:/Users/ALTAIR/Desktop/ParsingDodo/chromedriver-win64/chromedriver.exe')
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html')

with open('file.html', 'w' , encoding="utf-8") as file:
    file.write(str(soup))
# phones = soup.find('div', class_='vacancy-contacts-call-tracking__phone-number')
# print(phones)