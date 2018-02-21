# -*- coding: utf-8 -*-
import scrapy
import requests
from clint.textui import progress

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

        pdf = requests.get(url, stream=True)
        pdf.status_code
        if pdf.status_code == requests.codes.ok:
            print("Downloading file", local_filename)
            #self.log('Downloading filename:', local_filename)
        else:
            self.log("!!!Filed to download.!!!")
        #self.log('Downloading filename:', local_filename)
        self.log('Status Code:', pdf.status_code)
        #print('Start the download of %s: local_filename')

        with open(f'./books/{local_filename}', 'wb') as fd:
            total_size = int(pdf.headers.get('content-length'))
            print(total_size)
            for chunk in progress.bar(pdf.iter_content(chunk_size=1024),expected_size=(total_size/1024)+1):
                if chunk:
                    fd.write(chunk)
                    fd.flush()
            #for chunk in pdf.iter_content(1024):
                #fd.write(chunk)
                #self.log('writing chunk ')

