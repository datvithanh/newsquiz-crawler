# -*- coding: utf-8 -*-
import scrapy


class VietnamnewsSpider(scrapy.Spider):
    name = 'vietnamnews'
    allowed_domains = ['vietnamnews.vn']
    start_urls = ['http://vietnamnews.vn/']

    def parse(self, response):
        pass
