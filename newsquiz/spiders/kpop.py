# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
import datetime
from parsel import Selector
from newsquiz.items import ArticleItem
import re

class KpopSpider(scrapy.Spider):
    name = 'kpop'
    MAX_PAGE = 30

    def __init__(self):
        self.start_urls = ['http://kpoplove.koreadaily.com/category/news']
        self.page = 1
        self.crawling = True
        self.topic = 'kpop'
        self.crawled_date = 'None'
        self.set_crawled_date()

    def set_crawled_date(self):
        client = MongoClient('mongodb://newsquiz:grdVGACnq$2019@172.104.185.102:8600/admin?connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1')
        db = client['newsquiz']
        cur = db.articles.find({'publisher': self.name, 'topic': self.topic})
        docs = list(cur)
        publish_time = max([tmp['publish_time'] for tmp in docs], default='2015-01-01 00:00')

        self.crawled_date = datetime.datetime.strptime(publish_time, '%Y-%m-%d %H:%M')

    def parse(self, response):
        urls = response.xpath('//div[@class="td-ss-main-content"]/div/div/a/@href').extract()

        imgs = response.xpath('//div[@class="td-ss-main-content"]/div/div/a/img/@src').extract()

        for url, img in zip(urls, imgs):
            if self.crawling:
                yield scrapy.Request(url, callback=self.parse_article, meta={'thumbnail': img})

        if self.page < self.MAX_PAGE and self.crawling:
            self.page = self.page + 1
            yield scrapy.Request(f'http://kpoplove.koreadaily.com/category/news/page/{str(self.page)}/', callback=self.parse)
    
    def parse_article(self, response):
        title = response.xpath('//h1[@class="entry-title"]/text()').extract_first().strip()
        thumbnail = response.meta.get('thumbnail')
        published_time = response.xpath('//span[@class="td-post-date"]/time/text()').extract_first().strip()

        time = datetime.datetime.strptime(published_time, '%Y-%m-%d')
        if time < self.crawled_date:
            self.crawling = False
            return

        published_time = time.strftime('%Y-%m-%d %H:%M')
        
        author = 'None'
    
        html_content = response.xpath('//div[@class="td-post-content tagdiv-type"]').extract_first()

        html_content = re.sub(r'<span style="font-size: 12pt;">[.|\S|\s]*?<\/span>', '', html_content)

        content_p_tags = response.xpath('//div[@class="td-post-content tagdiv-type"]/p').extract()[:-3]      
        
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