# -*- coding: utf-8 -*-
# created: scrapy genspider books books.toscrape.com/

#import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

#use CrawlSpider instead
#class BooksSpider(scrapy.Spider):
class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com'] #note: not trailing /
    start_urls = ['http://books.toscrape.com/'] #note: www. is removed

    #rules variable of CrawlSpider
    #extract all links
    #note: quotes around callback
    #note: .self is not needed
    #note: follow is True to follow all subsequent linked URL pages
    #note: deny any possible related pages that can ban us, avoid possible social media pages
    #note: allow urls with 'music' included
    # <a href="catalogue/category/books/music_14/index.html">
    #note: use allow, deny_domains to be faster
    
    #LE = LinkExtractor(allow=('music'), deny_domains=('google.com') )
    LE = LinkExtractor()
    
    rules = ( Rule(LE, callback='parse_page', follow=False), )
    def parse_page(self, response):
        #pass
        #index urls
        yield {'URL' : response.url}

    #def parse(self, response):
    #    pass
