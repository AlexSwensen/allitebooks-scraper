# -*- coding: utf-8 -*-
import scrapy


class BookspiderSpider(scrapy.Spider):
    name = 'bookspider'
    allowed_domains = ['allitebooks.com']
    start_urls = ['http://allitebooks.com/']

    def parse(self, response):
        pass
