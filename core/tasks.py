import requests
from bs4 import BeautifulSoup

from celery import task

from core.models import NewsSource, News
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now

from core.parser import isna_parser


@task()
def news_crawler():
    print('task is executed!')
    sources = NewsSource.objects.filter(active=True)
    for source in sources:
        resp = requests.get(source.url)
        # print(resp)
        soup_xml = BeautifulSoup(resp.content, features="xml")
        items = soup_xml.findAll('item')
        source.last_crawl_date = now()
        source.save()
        for item in items:
            news_link = item.link.text
            url_handler.delay(news_link, source.id)
            # resp = requests.get(news_link)
            # soup_lxml = BeautifulSoup(resp.content, features="lxml")
            # title = soup_lxml.find('h1', class_='first-title')
            # # news_summery = soup_lxml.find('p', class_='summary')
            # news_text = soup_lxml.find('div', itemprop='articleBody')
            # news_id = soup_lxml.select_one('#item > div.news-info > div > ul > li:nth-child(3) > span.text-meta')
            # published_date = soup_lxml.find('meta', itemprop='datePublished')['content']


            # try:
            #     News.objects.create(
            #         url=news_link,
            #         title=title.text,
            #         source=source,
            #         news_id=news_id.text if news_id else None,
            #         content=news_text.text,
            #         published_at=parse_datetime(published_date)
            #     )
            # except Exception as e:
            #     print(e)




@task(name='isna_parser')
def url_handler(url: str, source_id: int):
    # check url is crawled
    duplicate_news = News.objects.filter(url=url).count()
    # crawl and make models
    if duplicate_news:
        return

    resp = requests.get(url)
    soup_lxml = BeautifulSoup(resp.content, features="lxml")
    title = soup_lxml.find('h1', class_='first-title')
    # news_summery = soup_lxml.find('p', class_='summary')
    news_text = soup_lxml.find('div', itemprop='articleBody')
    news_id = soup_lxml.select_one('#item > div.news-info > div > ul > li:nth-child(3) > span.text-meta')
    published_date = soup_lxml.find('meta', itemprop='datePublished')['content']

    try:
        News.objects.create(
            url=url,
            title=title.text,
            source=NewsSource.objects.get(id=source_id),
            news_id=news_id.text if news_id else None,
            content=news_text.text,
            published_at=parse_datetime(published_date)
        )
    except Exception as e:
        print(e)