# -*- coding: utf-8 -*-
import scrapy
import os
import time
from newsquiz.items import ArticleItem
from pymongo import MongoClient
from parsel import Selector

class EvnexpressSpider(scrapy.Spider):
    name = 'evnexpress'
    MAX_PAGE = 10
    ITEMS_PER_PAGE = None

    def __init__(self):
        self.name = 'evnexpress'
        self.start_urls = ['https://e.vnexpress.net/news/travel']
        self.allowed_url = 'https://e.vnexpress.net'
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

        self.crawled_date = time.strptime(publish_time, '%Y-%m-%d %H:%M')

    def parse(self, response):
        urls = [response.xpath('//div[@class="thumb_size thumb_left"]/a/@href').extract_first()] + response.xpath('//div[@id="vnexpress_folder_list_news"]/div/div/div/a/@href').extract()

        urls = [tmp for tmp in urls if not ('news/video' in tmp or 'infographics' in tmp or 'https://e.vnexpress.net/photo' in tmp)]
        # urls = ['https://e.vnexpress.net/news/travel/places/northern-vietnam-valley-unrolls-its-golden-carpet-3962891.html']

        for url in urls:
            if self.allowed_url in url and self.crawling:
                yield scrapy.Request(url, callback=self.parse_article)

        if self.page < self.MAX_PAGE and self.crawling:
            self.page = self.page + 1
            yield scrapy.Request(self.start_urls[0] + '?page=' + str(self.page), callback=self.parse)

    def parse_article(self, response):
        title = response.xpath('//h1[@class="title_post"]/text()').extract_first()
        thumbnail = response.xpath('//div[@class="thumb_detail_top"]/img/@src').extract_first()
        published_time = response.xpath('//meta[@name="pubdate"]/@content').extract_first()
        published_time = ' '.join(published_time.split(' ')[:2])

        if not thumbnail:
            thumbnail = response.xpath('//div[@class="fck_detail"]//img/@src').extract_first()


        if time.strptime(published_time, '%Y-%m-%d %H:%M') < self.crawled_date:
            self.crawling = False
            return

        author = response.xpath('//div[@class="author"]').extract_first()

        html_content = response.xpath('//div[@class="fck_detail"]').extract_first()
        
        content_p_tags = response.xpath('//div[@class="fck_detail"]/p').extract()
        
        content = []

        for p_tag in content_p_tags:
            sel = Selector(p_tag)
            texts = [tmp.replace('\n', '').replace('\t', '').replace('\r', '') for tmp in sel.xpath('//text()').extract()]
            texts = [tmp.strip() for tmp in texts if tmp.strip() != '']
            content.append(' '.join(texts))

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

        # TODO: logging    

class EvnexpressTravelSpider(EvnexpressSpider):
    name = 'evnexpress-travel'

    def __init__(self):
        EvnexpressSpider.__init__(self)
        self.start_urls = ['https://e.vnexpress.net/news/travel']
        self.topic = 'travel'

        self.set_crawled_date()

class EvnexpressBusinessSpider(EvnexpressSpider):
    name = 'evnexpress-business'

    def __init__(self):
        EvnexpressSpider.__init__(self)
        self.start_urls = ['https://e.vnexpress.net/news/business']
        self.topic = 'business'

        self.set_crawled_date()


class EvnexpressLifeSpider(EvnexpressSpider):
    name = 'evnexpress-life'

    def __init__(self):
        EvnexpressSpider.__init__(self)
        self.start_urls = ['https://e.vnexpress.net/news/life']
        self.topic = 'life'

        self.set_crawled_date()

class EvnexpressSportsSpider(EvnexpressSpider):
    name = 'evnexpress-sports'

    def __init__(self):
        EvnexpressSpider.__init__(self)
        self.start_urls = ['https://e.vnexpress.net/news/sports']
        self.topic = 'sports'

        self.set_crawled_date()