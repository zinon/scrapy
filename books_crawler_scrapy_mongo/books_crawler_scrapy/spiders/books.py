# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

import os, glob, csv

import pymongo


"""
prompt: scrapy shell 'http://books.toscrape.com/'
fetch: fetch('http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html') 

XPATH selector:
response.xpath('//h1').extract()
response.xpath('//h1/text()').extract()

CSS selector:
response.css('h1').extract()
response.css('h1::text').extract()

Run with arguments: scrapy crawl books -a category=http://books.toscrape.com

"""

class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com'] #no http:// and no ending /

    def __init__(self, category):
        self.start_urls = [category]

    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            abs_url = response.urljoin(book)
            yield Request(url = abs_url,
                          callback = self.parse_book)

        #process next page
        if False:
            next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
            abs_next_page_url = response.urljoin(next_page_url)
            yield Request(url = abs_next_page_url) #callback not needed
                      

    def prod_info(self, response, field):
        return response.xpath('//th[text()="%s"]/following-sibling::td/text()'%(field)).extract_first()

    def parse_book(self, response):
        domain = 'http://books.toscrape.com/'
        title = response.xpath('//h1/text()').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first() 
        image_url = response.xpath('//img/@src').extract_first()
        image_url = image_url.replace('../../', domain) 
        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.split(' ')[-1]

        description = response.xpath(
            '//*[@id="product_description"]/following-sibling::p/text()').extract_first()

        #product information
        upc = self.prod_info(response, 'UPC')
        availability = self.prod_info(response, 'Availability')

        #yield { 'title' : title,
        #        'price' : price,
        #        'image_url' : image_url,
        #        'rating' : rating,
        #        'description' : description,
        #        'upc' : upc,
        #        'availability' : availability }

        yield { 'title' : title,
                'price' : price.replace('£', ''),
                'upc' : upc,
                'availability' : availability }
