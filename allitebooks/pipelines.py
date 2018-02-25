# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter
import json
import pymongo
from scrapy import log

class AllitebooksPipeline(object):
    def process_item(self, item, spider):
        return item

class AlliteebooksJsonPipeline(object):
    def open_spider(self, spider):
        self.file = open("output.jsonl", 'w')
        self.exporter = JsonLinesItemExporter(self.file, encoding='utf8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def _exporter_for_item(self, item):
        return

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        #self.exporter.export_item(line)
        return item

class AllitebooksMongoDB(object):
    clection_name = 'ebooks_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABSE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.clection_name].insert_one(dict(item))
        log.msg("Ebook entry add to database!",level=log.DEBUG, spider=spider)
        return item