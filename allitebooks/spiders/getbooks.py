# -*- coding: utf-8 -*-
import scrapy
from requests import codes, get
from clint.textui import progress
from scrapy.loader import ItemLoader
from allitebooks.items import AllitebooksItem
import logging

logger = logging.getLogger('allitebookslogger')

class BookspiderSpider(scrapy.Spider):
    name = 'getbooks'
    allowed_domains = ['www.allitebooks.com']

    # start_urls = ['http://www.allitebooks.com']
    def start_requests(self):
        urls = ['http://www.allitebooks.com/']

        for i in range(2, 747):
            urls.append(f'http://www.allitebooks.com/page/{i}/')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        books = response.css('article')
        for book in books:
            book_body = book.css('.entry-body')
            book_link = book_body.css('a::attr(href)').extract_first()
            book_title = book_body.css('.entry-title a::text').extract_first()
            yield response.follow(book_link, callback=self.parse_book)

    def parse_book(self, response):
        loader = ItemLoader(item=AllitebooksItem(), response=response)

        title_body = response.css('header.entry-header')
        title = title_body.css('h1::text').extract_first()
        subtitle = title_body.css('h4::text').extract_first()
        metadata_entry = title_body.css('.entry-meta')
        thumbnail_url = metadata_entry.css('.entry-body-thumbnail a img::attr(src)').extract_first()
        book_detail = metadata_entry.css('.book-detail')
        footer = response.css('footer.entry-footer')
        download_link = footer.css('.download-links a::attr(href)').extract_first().replace(" ", "%20")
        #logger.log('Download Link -: %s')
        #logger.log("Download Link %s",download_link)
        print("link", download_link)

        loader.add_value('title', title)
        loader.add_value('subtitle', subtitle)
        loader.add_value('thumbnail_url', thumbnail_url)
        loader.add_value('download_link', download_link)

        return loader.load_item()