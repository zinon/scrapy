# -*- coding: utf-8 -*-
import scrapy

# for items.py
from scrapy import Spider
from scrapy.loader import ItemLoader

from simple_quotes_spider.items import SimpleQuotesSpiderItem

import random
from time import sleep
"""
creation: crapy genspider simple_quotes quotes.toscrape.com
use: scrapy crawl simple_quotes -s DOWNLOAD_DELAY=2

or enable sleep in code.

"""

class SimpleQuotesSpider(scrapy.Spider):
    name = 'simple_quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    
    def parse(self, response):
        """
        gets right-hand side tags
        """
        sleep( random.randrange(1, 3) )
        loader = ItemLoader(item = SimpleQuotesSpiderItem(),
                            response = response)
        
        h1_tag = response.xpath('//h1/a/text()').extract_first()
        tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()

        loader.add_value("h1_tag", h1_tag)
        loader.add_value("tags", tags)


        return loader.load_item()
