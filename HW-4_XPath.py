import requests
from pprint import pprint
from lxml import html
from pymongo import MongoClient
from datetime import date
from pymongo.errors import DuplicateKeyError as dke

client = MongoClient('127.0.0.1', 27017)
db = client['news_db']    # база данных
news_mon = db.news_mon        # коллекция

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
response = requests.get('https://yandex.ru/news')
dom = html.fromstring(response.text)

info = dom.xpath('//article')

news_id = 1
nl = []
for i in info:
    news = {}
    name = i.xpath('.//h2[@class="mg-card__title"]/text()')[0]
    link = i.xpath('.//a[@class="mg-card__link"]/@href')[0]
    source = i.xpath('.//a[@class="mg-card__source-link"]/text()')[0]
    time = i.xpath('.//span[@class="mg-card-source__time"]/text()')[0]
    n_date = f'{date.today()} {time}'

    news['_id'] = '00000' + str(news_id)
    news['name'] = name
    news['link'] = link
    news['source'] = source
    news['date'] = n_date

    nl.append(news)
    try:
        news_mon.insert_one(news)
    except dke:
        print(f"Документ с id = {news['_id']} уже существует в базе")
    news_id += 1
pprint(nl)
