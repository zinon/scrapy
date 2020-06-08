# -*- coding: utf-8 -*-
import scrapy

"""
scrapy crawl wiki -o results.csv
"""

class WikiSpider(scrapy.Spider):
    name = 'wiki'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population']

    def parse(self, response):
        table = response.xpath('//table[starts-with(@class, "wikitable sortable")]')[0]
        rows = table.xpath(".//tr")[1:]
        for row in rows:
            rank = row.xpath('.//td[1]/text()').extract_first().strip()

            #double slash //text() --> select all data
            city = row.xpath('.//td[2]//text()').extract_first()

            # | indicates an OR for another xpath
            state = row.xpath('.//*[@class="flagicon"]/following-sibling::a/text() | '
                              './/*[@class="flagicon"]/following-sibling::text()'
            ).extract_first().strip()

            yield { 'rank' : rank, 'city' : city, 'state' : state}
