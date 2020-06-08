# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

"""
Investigate:
scrapy shell "https://www.classcentral.com/subjects"
response.xpath('')

Run:
scrapy crawl classcentral
scrapy crawl classcentral -a subject='Programming'
scrapy crawl classcentral -a subject="Art & Design" -o art_and_design.csv
scrapy crawl classcentral -o all.csv
"""

class ClasscentralSpider(Spider):#scrapy.Spider):
    name = 'classcentral'
    allowed_domains = ['classcentral.com']
    start_urls = ['https://www.classcentral.com/subjects']


    def __init__(self, subject=None):
        self.__subject = subject
    
    def parse(self, response):
        if self.__subject:
            self.log('Scraping '+self.__subject)
            url = response.xpath('//a[contains(@title, "'+self.__subject+'")]/@href').extract_first()
            abs_url = response.urljoin(url)
            yield Request(abs_url, callback=self.parse_url)
        else:
            self.log('Scraping all subjects...')
            #select only 1st a-tag
            urls = response.xpath('//h3/a[1]/@href').extract()
            for url in urls:
                abs_url = response.urljoin(url)
                yield Request(abs_url, callback=self.parse_url)
            
    def parse_url(self, response):
        
        subject_name = response.xpath('//h1/text()').extract_first()

        courses = response.xpath('//tr[@itemtype="http://schema.org/Event"]')

        for course in courses:
            course_name = course.xpath('.//*[@itemprop="name"]/text()').extract_first().strip()
            course_url = course.xpath('.//a[@itemprop="url"]/@href').extract_first().strip()
            abs_course_url = response.urljoin(course_url)

            yield {
                'subject' :  subject_name,
                'course': course_name,
                'url' : abs_course_url
                }

            next_page = response.xpath('//link[@rel="next"]/@href').extract_first()

            if next_page:
                abs_next_page = response.urljoin(next_page)
                yield Request(abs_next_page, callback = self.parse_url)
