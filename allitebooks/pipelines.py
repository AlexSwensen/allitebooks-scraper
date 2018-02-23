# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter
import json

class AllitebooksPipeline(object):
    def process_item(self, item, spider):
        return item

class AlliteebooksJsonPipeline(object):
    def __init__(self):
        self.file = open("output2.json", 'wb')

    def open_spider(self, spider):

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
        #self.exporter.export_item(item)
        return item