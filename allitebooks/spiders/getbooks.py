# -*- coding: utf-8 -*-
import scrapy
import requests


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
        metadata_entry = title_body.css('.entry-meta')
        thumbnail_url = metadata_entry.css('.entry-body-thumbnail a img::attr(src)').extract_first()
        book_detail = metadata_entry.css('.book-detail')
        footer = response.css('footer.entry-footer')
        download_link = footer.css('.download-links a::attr(href)').extract_first()

        self.download_file(download_link)


    def download_file(self, url):
        local_filename = url.split('/')[-1]
        pdf = requests.get(url)
