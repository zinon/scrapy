# -*- coding: utf-8 -*-
# created: scrapy genspider books books.toscrape.com/
#
# Scraping with Selenium + Scrapy
#
# wget -N http://chromedriver.storage.googleapis.com/<?>/chromedriver_linux64.zip
# unzip chromedriver_linux64.zip
# chmod +x chromedriver

#driver = webdriver.Chrome('/home/zinonas/Downloads/chromedriver')
#driver = webdriver.Chrome(ChromeDriverManager().install())
#driver.get('http://google.com')
#driver.title
#driver.page_source 

from scrapy import Spider
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
#selector from scraping urls
from scrapy.selector import Selector

#requests
from scrapy.http import Request

#sleep
from time import sleep
import random

#get data (adjust item.py)
from books_crawler.items import BooksCrawlerItem

class BooksSpider(Spider):

    name = 'books'
    allowed_domains = ['books.toscrape.com'] #note: not trailing /

    #searched by Spider
    def start_requests(self):
        self.driver = webdriver.Chrome('/home/zinonas/Downloads/chromedriver')
        self.driver.get('http://books.toscrape.com')

        #pre-append domain url
        #can be used also as:
        #book_urls = ['%s%s'%(domain, i) for i in book_urls]
        domain = 'http://books.toscrape.com/'
        domain_cat = 'http://books.toscrape.com/catalogue/'

        #get urls from source page obtained with selenium
        #<h3>
        #   <a> href='...'
        #Note: the first pages has the dir 'catalogue' in the url
        sel = Selector(text = self.driver.page_source)
        book_urls = sel.xpath('//h3/a/@href').extract() 
        for url in book_urls:
            url = domain + url
            yield Request(url = url, callback=self.parse_book)

        while True:
            try:
                next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
                seconds = random.randrange(3, 5)
                self.logger.info('Sleeping for %f secs...'%(seconds))
                sleep( seconds )
                next_page.click()

                #Note: the next pages have not the dir 'catalogue' in the url
                sel = Selector(text = self.driver.page_source)
                book_urls = sel.xpath('//h3/a/@href').extract() 
                for url in book_urls:
                    url = domain_cat + url
                    yield Request(url = url, callback=self.parse_book)
                
            except NoSuchElementException:
                self.logger.info('No more pages to load')
                self.driver.quit()
                break
    def parse_book(self, response):
        #pass
        items = BooksCrawlerItem()
        title = response.css('h1::text').extract_first()
        url = response.request.url

        items['title'] = title
        items['url'] = url
        yield items
