import requests
from bs4 import BeautifulSoup

from celery import task

from core.models import NewsSource, News
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now


@task()
def news_crawler():
    print('task is executed!')
    sources = NewsSource.objects.filter(active=True)
    for source in sources:
        resp = requests.get(source.url)
        print(resp)
        soup_xml = BeautifulSoup(resp.content, features="xml")
        items = soup_xml.findAll('item')
        source.last_crawl_date = now()
        source.save()
        for item in items:
            print(11111111)
            news_link = item.link.text
            resp = requests.get(news_link)
            print(2222222222)
            soup_lxml = BeautifulSoup(resp.content, features="lxml")
            title = soup_lxml.find('h1', class_='first-title')
            print(33333333333)

            # news_summery = soup_lxml.find('p', class_='summary')
            news_text = soup_lxml.find('div', itemprop='articleBody')
            print(44444444444)
            news_id = soup_lxml.select_one('#item > div.news-info > div > ul > li:nth-child(3) > span.text-meta')
            published_date = soup_lxml.find('meta', itemprop='datePublished')['content']
            print(55555555555555)
            print(parse_datetime(published_date))

            print(news_link)
            print(title.text)
            print(news_text.text)

            # News.objects.create(
            #     url=news_link,
            #     title=title.text,
            #     source=source,
            #     news_id=news_id,
            #     content=news_text.text,
            #     # published_at=parse_datetime(published_date),
            # )