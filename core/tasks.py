import requests
import json
from bs4 import BeautifulSoup

from celery import task

from core.models import NewsSource, News
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now

from core.parser import isna_parser


@task()
def news_crawler():
    print(000000000000)
    sources = NewsSource.objects.filter(active=True)
    for source in sources:
        resp = requests.get(source.url)
        soup_xml = BeautifulSoup(resp.content, features="xml")
        items = soup_xml.findAll('item')
        source.last_crawl_date = now()
        source.save()
        for item in items:
            news_link = item.link.text
            url_handler.delay(news_link, source.id)



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
    news_summery = soup_lxml.find('p', class_='summary').text
    main_image = soup_lxml.select_one('#item > div.full-news > div.full-news-text > div.item-body.content-full-news > figure > img')
    header_data = []
    if main_image:
        main_image_source = main_image['src']
        header_data.append({'image': str(main_image_source)})
    header_data.append({'normal': str(news_summery)})
    news_parsed_data = isna_parser(str(soup_lxml.find('div', itemprop='articleBody')))
    news_data = [{'p': header_data}] + news_parsed_data
    news_json_data = json.dumps(news_data)
    news_id = soup_lxml.select_one('#item > div.news-info > div > ul > li:nth-child(3) > span.text-meta')
    published_date = soup_lxml.find('meta', itemprop='datePublished')['content']

    try:
        News.objects.create(
            url=url,
            title=title.text,
            source=NewsSource.objects.get(id=source_id),
            news_id=news_id.text if news_id else None,
            content=news_json_data,
            published_at=parse_datetime(published_date)
        )
    except Exception as e:
        print(e)