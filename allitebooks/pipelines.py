# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter
import json
import pymongo
from scrapy import log
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
import scrapy

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

class AllitebooksImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for thumbnail_url in item['thumbnail_url']:
            yield scrapy.Request(thumbnail_url)

    def item_completed(self, results, item, info):
        thumbnail_url = [x['path'] for ok, x in results if ok]
        if not thumbnail_url:
            raise DropItem("Item contains no images")
        item['thumbnail_url'] = thumbnail_url
        return item

class AllitebooksFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        for download_link in item['download_link']:
            yield scrapy.Request(download_link)

    def item_completed(self, results, item, info):
        download_link = [x['path'] for ok, x in results if ok]
        if not download_link:
            raise DropItem("Item contains no Files")
        item['download_link'] = download_link
        return item