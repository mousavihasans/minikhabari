import traceback

import requests
import json
from bs4 import BeautifulSoup

from celery import task

from core.models import NewsSource, News, ErrorTracker
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now

from core.parser import isna_parser


@task()
def news_crawler():
    sources = NewsSource.objects.filter(active=True)
    for source in sources:
        news_link = None
        try:

            resp = requests.get(source.url)
            soup_xml = BeautifulSoup(resp.content, features="xml")
            items = soup_xml.findAll('item')
            source.last_crawl_date = now()
            source.save()
            for item in items:
                news_link = item.link.text
                url_handler.delay(news_link, source.id)
        except Exception as e:
            print(traceback.format_exc())
            e_data = dict()
            e_data['source'] = source
            e_data['e_data'] = str(traceback.format_exc())
            if news_link:
                e_data['news_link'] = news_link

            ErrorTracker.objects.create(
                error_name=str(e),
                extra_data=e_data
            )


@task(name='isna_parser')
def url_handler(url: str, source_id: int):
    # check whether the url is crawled
    # todo: make a contemporary cache of it
    duplicate_news = News.objects.filter(url=url).count()
    if duplicate_news:
        return

    # crawl and create models
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
    news_content = str(soup_lxml.find('div', itemprop='articleBody'))[46:-6]  # remove outer tag
    news_parsed_data = isna_parser(news_content)
    news_data = [{'p': header_data}] + news_parsed_data
    news_json_data = json.dumps(news_data)
    news_id = soup_lxml.select_one('#item > div.news-info > div > ul > li:nth-child(3) > span.text-meta')
    published_date = soup_lxml.find('meta', itemprop='datePublished')['content']

    News.objects.create(
        url=url,
        title=title.text,
        source=NewsSource.objects.get(id=source_id),
        news_id=news_id.text if news_id else None,
        content=news_json_data,
        published_at=parse_datetime(published_date)
    )

