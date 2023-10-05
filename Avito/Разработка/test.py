from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
import random
import time
import csv
import datetime
from bs4 import BeautifulSoup

driver = webdriver.Chrome('C:/AvitoParser.py/chromedriver-win64/chromedriver.exe')
driver.get('https://www.avito.ru/brands/i165731750/all/vakansii?gdlkerfdnwq=101&shopId=260382&iid=3364619822&page_from=from_item_header&sellerId=937b3437f5ffb54d93f1cc0b20dbfe61')

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

import scrapy
from datetime import datetime
from scrapy.crawler import CrawlerProcess


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    start_urls = [line.strip() for line in open('LinksForParser.txt', 'r')]

    def parse(self, response):
        vacancies = response.css('div.iva-item-root-_lk9K')

        for vacancy in vacancies:
            try:
                job_title = vacancy.css('[itemprop="name"]::text').get()
                salary = "".join(vacancy.css('p.styles-module-root-_KFFt strong::text').getall())
                full_link = response.urljoin(vacancy.css('[itemprop="url"]::attr(href)').get())
                city = vacancy.css('div.geo-root-zPwRk p::text').get()

                yield {
                    'Job Title': job_title,
                    'Salary': salary,
                    'Link': full_link,
                    'City': city,
                    'Scrape Time': datetime.now().strftime("%d.%m.%Y"),
                }
            except AttributeError:
                continue

        next_page = response.css('a.pagination-page_next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


process = CrawlerProcess(settings={'FEED_FORMAT': 'csv', 'FEED_URI': 'vacancy_data_avito.csv'})
process.crawl(AvitoSpider)
process.start()

date_all = soup.find_all('div', class_ = 'styles-module-root-SfSd4 styles-module-margin-top_none-urOXk styles-module-margin-bottom_none-YEOJI')
print(date_all)

