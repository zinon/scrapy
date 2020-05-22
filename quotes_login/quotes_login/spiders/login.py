# -*- coding: utf-8 -*-
import scrapy

#import from request for POST
from scrapy.http import FormRequest

from scrapy.utils.response import open_in_browser

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        """
        Headers > General > Request URL
        Headers > Form Data
        """
        url = 'http://quotes.toscrape.com/login'

        #
        csrf_token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()
        
        fdata = {'csrf_token' : csrf_token,
                 'username' : 'user',
                 'password' : 'passw'}
        

        yield FormRequest(url = url,
                          formdata=fdata,
                          callback=self.parse_after_login)

    def parse_after_login(self, response):
        #if looged successfully, open new tab in browser
        open_in_browser(response)

        #or print out a message
        #if response.xpath('//a[text()="Logout"]'):
        #    self.log("Logged in!")
