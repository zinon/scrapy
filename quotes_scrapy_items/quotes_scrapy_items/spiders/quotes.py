# -*- coding: utf-8 -*-
import scrapy

import os, glob, csv
from  openpyxl import Workbook

from quotes_scrapy_items.items import QuotesScrapyItemsItem
"""
scrapy startproject quotes_scrapy_items
cd quotes_scrapy_items

Live Testing:
scrapy shell 'http://quotes.toscrape.com/'

Generate:
scrapy genspider quotes quotes.toscrape.com

Run:
scrapy crawl quotes -o items.csv


"""
class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/'] #remove www

    def parse(self, response):
        authors = response.xpath('//*[@itemprop="author"]/text()').extract() 
        
        #yield {'authors' : authors}
        
        item = QuotesScrapyItemsItem()
        item['authors'] = authors
        return item

    def close(self, reason):

        csv_file = max( glob.iglob('*.csv'), key=os.path.getctime )
        print('Picked file', csv_file)
        print('Save excel file')
        wb = Workbook()
        ws = wb.active

        with open(csv_file, 'r') as f:
            for row in csv.reader(f):
                ws.append(row)

        wb.save(csv_file.replace('.csv', '.xlsx') )
