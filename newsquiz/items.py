# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsquizItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    topic = scrapy.Field()
    url = scrapy.Field()
    thumbnail = scrapy.Field()
    content = scrapy.Field()
    content_raw = scrapy.Field()
    publish_time = scrapy.Field()
    publisher = scrapy.Field()
    author = scrapy.Field()