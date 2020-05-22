# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

#items
from scrapy.loader import ItemLoader
from books_crawler_scrapy.items import BooksCrawlerScrapyItem


"""
prompt: scrapy shell 'http://books.toscrape.com/'
fetch: fetch('http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html') 

XPATH selector:
response.xpath('//h1').extract()
response.xpath('//h1/text()').extract()

CSS selector:
response.css('h1').extract()
response.css('h1::text').extract()

Run: scrapy crawl books -o books.csv -a navigate=True

Note: enable ITEM_PIPELINES in settings.py
"""

class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com'] #no http:// and no ending /
    start_urls = ['http://books.toscrape.com/']

    def __init__(self, navigate):
        self.navigate = navigate

    
    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            abs_url = response.urljoin(book)
            yield Request(url = abs_url,
                          callback = self.parse_book)

        #process next page
        if self.navigate:
            next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
            abs_next_page_url = response.urljoin(next_page_url)
            yield Request(url = abs_next_page_url) #callback not needed
                      

    def prod_info(self, response, field):
        #product information
        return response.xpath('//th[text()="%s"]/following-sibling::td/text()'%(field)).extract_first()

    def parse_book(self, response):
        l = ItemLoader(item = BooksCrawlerScrapyItem(),
                       response = response)
        
        domain = 'http://books.toscrape.com/'

        #pipelined items
        title = response.xpath('//h1/text()').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first() 

        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.split(' ')[-1]

        description = response.xpath(
            '//*[@id="product_description"]/following-sibling::p/text()').extract_first()

        upc = self.prod_info(response, 'UPC')
        availability = self.prod_info(response, 'Availability')


        image_urls = response.xpath('//img/@src').extract_first()
        image_urls = image_urls.replace('../../', domain) 

        l.add_value('title', title)
        l.add_value('price', price)
        l.add_value('rating', rating)
        l.add_value('image_urls', image_urls)

        return l.load_item()
        

