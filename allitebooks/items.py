# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AllitebooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    thumbnail_url = scrapy.Field()
    download_link = scrapy.Field()
    downloads = scrapy.Field()

