import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from time import sleep

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
}

data = []

def extract_data(url):
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"Failed to load page {url}. Ending program.")
        sys.exit(1)
    sleep(3)
    soup = BeautifulSoup(r.text, 'lxml')
    classSearchs = soup.find_all('div', class_='_awwm2v')[1]

    for classSearch in classSearchs:
        try:
            names = classSearch.find('div', class_='_zjunba').text.strip()
        except:
            names = ' '
        try:
            int: ratings = classSearch.find('div', class_='_y10azs').text.strip()
        except:
            ratings = ' '
        try:
            ratingss = classSearch.find('div', class_='_jspzdm').text.strip()
        except:
            ratingss = ' '
        try:
            city_links = 'https://2gis.ru' + classSearch.find('div', class_='_klarpw').find('a')['href'].strip()
        except:
            city_links = ' '
        try:
            full_Links = 'https://2gis.ru' + classSearch.find('div', class_='_xcqknf').find('a')['href'].strip()
        except:
            full_Links = ' '
        try:
            city = classSearch.find('div', class_='_klarpw').text.strip()
        except:
            city = ' '
        try:
            chekmedian = classSearch.find('div', class_='_d76pv4').text.strip()
        except:
            chekmedian = ' '
        try:
            links = classSearch.find('div', class_='_xcqknf').text.strip()
        except:
            links = ' '

        Timestamp = datetime.now().strftime('%d.%m.%Y')

        data.append([names, ratings,ratingss, city_links, full_Links, city, chekmedian, links, Timestamp])

# Создание списка URL
urls = [f'https://2gis.ru/search/Пиццерии/page/{p}?m=77.044126%2C61.661587%2F4.08%2Fp%2F5.18%2Fd%2F4.77' for p in range(1, 2)]

# Использование ThreadPoolExecutor для выполнения функции extract_data для каждого URL одновременно
with ThreadPoolExecutor() as executor:
    executor.map(extract_data, urls)

df = pd.DataFrame(data, columns=['names','ratings', 'ratingss', 'city_links','full_Links','city','chekmedian','links','Timestamp'])

# Сохранение DataFrame в файл CSV
with open('data2Gis.csv','w', encoding='utf-8') as f:
    df.to_csv(f, index=False)