# -*- coding: utf-8 -*-
import scrapy


class BookspiderSpider(scrapy.Spider):
    name = 'getbooks'
    allowed_domains = ['www.allitebooks.com']
    # start_urls = ['http://www.allitebooks.com']
    def start_requests(self):
        urls = ['http://www.allitebooks.com/']

        for i in range(2, 747):
            urls.append(f'http://www.allitebooks.com/page/{i}/')

        self.log(urls)

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
        title_body = response.css('header.entry-header')
        title = title_body.css('h1::text').extract_first()
        subtitle = title_body.css('h4::text').extract_first()
