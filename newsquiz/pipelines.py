# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from pymongo import MongoClient
import uuid
import datetime
import numpy as np
from scrapy.exceptions import DropItem


class NewsquizPipeline(object):
    def __init__(self):
        client = MongoClient('mongodb://newsquiz:grdVGACnq$2019@172.104.185.102:8600/admin?connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1')
        self.db = client['newsquiz']
        cur = self.db.articles.find()
        docs = list(cur)

        self.exist_articles = set([tmp['title'] + tmp['publisher'] + tmp ['topic'] for tmp in docs])
    
    def generate_filename(self):
        fname = uuid.uuid5(uuid.NAMESPACE_OID, str(datetime.datetime.now()))
        return str(fname).replace('-', '')

    def save_article(self, article):
        final_article = {}
        # title, topic, created_time, source_url, content, publisher, id, level, thumbnail, audio, type
        final_article['title'] = article['title']
        final_article['topic'] = article['topic']
        final_article['created_time'] = datetime.datetime.utcnow()
        final_article['source_url'] = article['url']
        final_article['content'] = article['content']
        final_article['content_raw'] = article['content_raw']
        final_article['publisher'] = article['publisher']
        final_article['id'] = self.generate_filename()
        final_article['level'] = np.random.choice(['easy', 'medium', 'hard'])
        final_article['thumbnail'] = article['thumbnail']
        final_article['audio'] = ''
        final_article['type'] = 'text'
        final_article['publish_time'] = article['publish_time']

        self.db.articles.insert_one(final_article)


    def process_item(self, item, spider):
        if item['title'] + item['publisher'] + item['topic'] in self.exist_articles:
            raise DropItem(f'Duplicated item found {item["title"]}')
        else:
            self.exist_articles.add(item['title'] + item['publisher'] + item['topic'])
            self.save_article(item)
            return True
