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

        print(urls)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'books-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
