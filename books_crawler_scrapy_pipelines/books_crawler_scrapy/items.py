# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BooksCrawlerScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    title = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    upc = scrapy.Field()
    availability = scrapy.Field()
    
    image_urls = scrapy.Field()
    images = scrapy.Field()

    

