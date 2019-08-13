# -*- coding: utf-8 -*-
import scrapy
import os
import time
from newsquiz.items import ArticleItem
from pymongo import MongoClient
from parsel import Selector
import datetime

class VietnamnewsSpider(scrapy.Spider):
    name = 'vietnamnews'
    MAX_PAGE = 10
    ITEMS_PER_PAGE = None

    def __init__(self):
        self.name = 'vietnamnews'
        self.start_urls = ['https://vietnamnews.vn/politics-laws']
        self.allowed_url = 'https://vietnamnews.vn'
        self.page = 1
        self.crawling = True
        self.topic = 'None'
        self.crawled_date = 'None'

    def set_crawled_date(self):
        client = MongoClient('mongodb://newsquiz:grdVGACnq$2019@172.104.185.102:8600/admin?connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1')
        db = client['newsquiz']
        cur = db.articles.find({'publisher': self.name, 'topic': self.topic})
        docs = list(cur)
        publish_time = max([tmp['publish_time'] for tmp in docs], default='2015-01-01 00:00')

        self.crawled_date = datetime.datetime.strptime(publish_time, '%Y-%m-%d %H:%M')

    def parse(self, response):
        urls = response.xpath('//div[@class="vnnews-list-news"]/ul/li/a/@href').extract()

        imgs = response.xpath('//div[@class="vnnews-list-news"]/ul/li/a/span/img/@src').extract()

        urls = [self.allowed_url + tmp for tmp in urls]

        for url, img in zip(urls, imgs):
            if self.allowed_url in url and self.crawling:
                yield scrapy.Request(url, callback=self.parse_article, meta={'thumbnail': img})

        if self.page < self.MAX_PAGE and self.crawling:
            self.page = self.page + 1
            yield scrapy.Request(self.start_urls[0] + '?p=' + str(self.page), callback=self.parse)

    def parse_article(self, response):
        title = response.xpath('//h3[@class="vnnews-tt-post"]/text()').extract_first().strip()
        thumbnail = response.meta.get('thumbnail')
        published_time = response.xpath('//div[@class="vnnews-time-post"]/span/text()').extract_first().strip()
        time = datetime.datetime.strptime(published_time, '%B, %d/%Y - %H:%M')
        if time < self.crawled_date:
            self.crawling = False
            return
            
        published_time = time.strftime('%Y-%m-%d %H:%M')

        author = 'None'
        
        try:
            author = response.xpath('//span[@class="vnnews-user-post"]/text()').extract_first().strip()
        except:
            author = 'None'

        html_content = response.xpath('//div[@class="vnnews-text-post"]').extract_first()

        content_p_tags = response.xpath('//div[@class="vnnews-text-post"]/div/p').extract()        

        if len(content_p_tags) <= 2:
            content_p_tags = response.xpath('//div[@class="vnnews-text-post"]/p').extract()
        
        content = []

        for p_tag in content_p_tags:
            sel = Selector(p_tag)
            texts = [tmp.replace('\n', '').replace('\t', '').replace('\r', '') for tmp in sel.xpath('//text()').extract()]
            texts = [tmp.strip() for tmp in texts if tmp.strip() != '']
            content.append(' '.join(texts))

        content = '\n'.join([tmp for tmp in content if tmp != ''])
        
        if content.strip() == '':
            return
        
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

        # TODO: logging    

class VietnamnewsPoliticsLawsSpider(VietnamnewsSpider):
    name = 'vietnamnews-politics-laws'

    def __init__(self):
        VietnamnewsSpider.__init__(self)
        self.start_urls = ['https://vietnamnews.vn/politics-laws']
        self.topic = 'politics'

        self.set_crawled_date()

class VietnamnewsSocietySpider(VietnamnewsSpider):
    name = 'vietnamnews-society'

    def __init__(self):
        VietnamnewsSpider.__init__(self)
        self.start_urls = ['https://vietnamnews.vn/society']
        self.topic = 'society'

        self.set_crawled_date()

class VietnamnewsEconomySpider(VietnamnewsSpider):
    name = 'vietnamnews-economy'

    def __init__(self):
        VietnamnewsSpider.__init__(self)
        self.start_urls = ['https://vietnamnews.vn/economy']
        self.topic = 'economy'

        self.set_crawled_date()

class VietnamnewsLifestyleSpider(VietnamnewsSpider):
    name = 'vietnamnews-lifestyle'

    def __init__(self):
        VietnamnewsSpider.__init__(self)
        self.start_urls = ['https://vietnamnews.vn/life-style']
        self.topic = 'lifestyle'

        self.set_crawled_date()

class VietnamnewsSportsSpider(VietnamnewsSpider):
    name = 'vietnamnews-sports'

    def __init__(self):
        VietnamnewsSpider.__init__(self)
        self.start_urls = ['https://vietnamnews.vn/sports']
        self.topic = 'sports'

        self.set_crawled_date()

class VietnamnewsEnvironmentSpider(VietnamnewsSpider):
    name = 'vietnamnews-environment'

    def __init__(self):
        VietnamnewsSpider.__init__(self)
        self.start_urls = ['https://vietnamnews.vn/environment']
        self.topic = 'environment'

        self.set_crawled_date()