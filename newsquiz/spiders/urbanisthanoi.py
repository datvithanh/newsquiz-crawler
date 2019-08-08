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
        self.domain = 'http://urbanisthanoi.com'
        self.allowed_domains = ['urbanisthanoi.com']
        self.start_urls = ['http://urbanisthanoi.com/eat-drink']

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
        urls = [response.xpath('//div[@class="leading leading-0"]//h2/a/@href').extract_first()] +  [response.xpath('//div[@class="span6"]//div[@class="contentpaneopen"]/h2[@class="contentheading"]/a/@href').extract()]

        if not urls:
            self.crawling = False

        for url in urls:
            if self.crawling:
                yield scrapy.Request(self.domain + url, callback=self.parse_article)
                break

        # if self.page <= self.MAX_PAGE and self.crawling:
        #     self.page = self.page + 1
        #     yield scrapy.Request(self.start_urls[0] + '?start=' + str((self.page-1) * self.ITEMS_PER_PAGE), callback=self.parse)

    def parse_article(self, response):
        title = response.xpath('//h1[@class="contentheading"]/a/text()').extract_first().strip()

        thumbnail = response.xpath('//img[@class="progressiveMedia-thumbnail"]/@src').extract_first()[2:-5] + 'l.jpg'

        published_time = response.xpath('//dd[@class="published"]/text()').extract_first().split(',')[-1].strip()
        time = datetime.datetime.strptime(published_time, '%d %B %Y %H:%M')
        published_time = time.strftime('%Y-%m-%d %H:%M')

        print(published_time)

        # if time.strptime(published_time, '%Y-%m-%d %H:%M') < self.crawled_date:
        #     self.crawling = False
        #     return

        author = response.xpath('//dd[@class="createdby"]/text()').extract_first().split('.')[0].strip()[11:]
        print(author)
        html_content = response.xpath('//div[@class="item-page"]').extract_first()
        content_text = [tmp.replace('\n', '').replace('\t', '').replace('\r', '') for tmp in response.xpath('//div[@class="item-page"]/p//text()').extract()]
        print(content_text)
        content = []
        para = ''
        for tmp in content_text:
            if para.strip().endswith('.') or para.strip().endswith(':') or para.strip()[-1].isdigit():
                content.append(para)
                para = tmp
            else:
                para += tmp

        content.append(para)

        for tmp in content:
            print(tmp)

        # html_content = '\n'.join([tmp for tmp in content if tmp != ''])

        # # store item
        # item = ArticleItem()
        # item['topic'] = self.topic
        # item['title'] = title
        # item['url'] = response.url
        # item['thumbnail'] = thumbnail
        # item['html_content'] = html_content
        # item['publish_time'] = published_time
        # item['publisher'] = self.name
        # item['author'] = author
        # yield item

"""
TODO: 
-   run multiple spider at a same time
-   periodically call the spider somehow
"""