# -*- coding: utf-8 -*-
import scrapy
import os
import datetime
import time
from newsquiz.items import ArticleItem
from pymongo import MongoClient

class UrbanisthanoiSpider(scrapy.Spider):
    name = 'urbanisthanoi'
    MAX_PAGE = 10
    ITEMS_PER_PAGE = 11

    def __init__(self):
        self.name = 'urbanisthanoi'
        self.domain = 'https://urbanisthanoi.com'
        self.allowed_domains = ['urbanisthanoi.com']
        self.start_urls = ['https://urbanisthanoi.com/eat-drink']

        self.page = 1
        self.crawling = True
        self.topic = None
        self.crawled_date = None
        

    def set_crawled_date(self):
        client = MongoClient('mongodb://newsquiz:grdVGACnq$2019@172.104.185.102:8600/admin?connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1')
        db = client['newsquiz']
        cur = db.articles.find({'publisher': self.name, 'topic': self.topic})
        docs = list(cur)
        publish_time = max([tmp['publish_time'] for tmp in docs], default='2015-01-01 00:00')

        self.crawled_date = time.strptime(publish_time, '%Y-%m-%d %H:%M')

    def parse(self, response):
        urls = [response.xpath('//div[@class="leading leading-0"]//h2/a/@href').extract_first()] +  response.xpath('//div[@class="span6"]//div[@class="contentpaneopen"]/h2[@class="contentheading"]/a/@href').extract()

        if not urls:
            self.crawling = False
        print(urls)
        for url in urls:
            if self.crawling:
                yield scrapy.Request(self.domain + url, callback=self.parse_article)

        if self.page <= self.MAX_PAGE and self.crawling:
            self.page = self.page + 1
            yield scrapy.Request(self.start_urls[0] + '?start=' + str((self.page-1) * self.ITEMS_PER_PAGE), callback=self.parse)

    def parse_article(self, response):
        title = response.xpath('//h1[@class="contentheading"]/a/text()').extract_first().strip()
        if title.strip().startswith('[Photos]') or title.strip().startswith('[Video]'):
            return
        thumbnail = response.xpath('//img[@class="progressiveMedia-thumbnail"]/@src').extract_first()[2:-5] + 'l.jpg'

        published_time = response.xpath('//dd[@class="published"]/text()').extract_first().split(',')[-1].strip()
        time = datetime.datetime.strptime(published_time, '%d %B %Y %H:%M')
        published_time = time.strftime('%Y-%m-%d %H:%M')

        author = response.xpath('//dd[@class="createdby"]/text()').extract_first().split('.')[0].strip()[11:]
        # TODO: clean this shit
        html_content = response.xpath('//div[@class="item-page"]').extract_first()
        content_text = [tmp.replace('\n', '').replace('\t', '').replace('\r', '').replace('\xa0', '') for tmp in response.xpath('//div[@class="item-page"]/p//text()').extract()]

        content = []
        para = ''
        for tmp in content_text:
            if para.strip().endswith('.') or para.strip().endswith(':'):
                content.append(para)
                para = tmp
            else:
                para += ' ' + tmp.strip()

        content.append(para)

        content = '\n'.join([tmp for tmp in content if tmp != ''])

        # store item
        item = ArticleItem()
        item['topic'] = self.topic
        item['title'] = title
        item['url'] = response.url
        item['thumbnail'] = thumbnail
        item['content'] = content
        item['content_raw'] = html_content
        item['publish_time'] = published_time
        item['publisher'] = self.name
        item['author'] = author
        yield item

class UrbanisthanoiArtsCultureSpider(UrbanisthanoiSpider):
    name = 'urbanisthanoi-hanoi-arts-culture'

    def __init__(self):
        UrbanisthanoiSpider.__init__(self)
        self.start_urls = ['https://urbanisthanoi.com/hanoi-arts-culture']
        self.topic = 'hanoi-arts-culture'

        self.set_crawled_date()

class UrbanisthanoiEatDrinkSpider(UrbanisthanoiSpider):
    name = 'urbanisthanoi-eat-drink'

    def __init__(self):
        UrbanisthanoiSpider.__init__(self)
        self.start_urls = ['https://urbanisthanoi.com/eat-drink']
        self.topic = 'eat-drink'

        self.set_crawled_date()

class UrbanisthanoiNewsSpider(UrbanisthanoiSpider):
    name = 'urbanisthanoi-news'

    def __init__(self):
        UrbanisthanoiSpider.__init__(self)
        self.start_urls = ['http://urbanisthanoi.com/news']
        self.topic = 'urbanisthanoi-news'

        self.set_crawled_date()

class UrbanisthanoiSocietySpider(UrbanisthanoiSpider):
    name = 'urbanisthanoi-society'

    def __init__(self):
        UrbanisthanoiSpider.__init__(self)
        self.start_urls = ['http://urbanisthanoi.com/society']
        self.topic = 'society'

        self.set_crawled_date()

class UrbanisthanoiOldHanoiSpider(UrbanisthanoiSpider):
    name = 'urbanisthanoi-old-hanoi'

    def __init__(self):
        UrbanisthanoiSpider.__init__(self)
        self.start_urls = ['http://urbanisthanoi.com/old-hanoi']
        self.topic = 'old-hanoi'

        self.set_crawled_date()


"""
TODO: 
-   run multiple spider at a same time
-   periodically call the spider somehow
"""