# -*- coding: utf-8 -*-
"""
Run:

sudo docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash
scrapy crawl quotes -o results.csv

"""

import scrapy


from scrapy_splash import SplashRequest

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/js/']

    def start_requests(self):
        #iterate over starting URLs
        #Return the HTML of the javascript-rendered page.
        #Ref: https://splash.readthedocs.io/en/stable/api.html#render-html
        for url in self.start_urls:
            yield SplashRequest(url = url,
                                callback = self.parse,
                                endpoint = 'render.html') 
    def parse(self, response):
        quotes = response.xpath('//*[@class="quote"]')

        for quote in quotes:
            #use .// (dot) when using the custom selector 'quote' rather the default 'response'
            #use * to select every html node
            author = quote.xpath('.//*[@class="author"]/text()').extract_first()
            quote = quote.xpath('.//*[@class="quote"]/text()').extract_first()
            yield { 'author' : author, 
                    'quote' : quote
            }

        #navigate through 'next' pages using Lua code
        #see https://splash.readthedocs.io/en/stable/scripting-tutorial.html
        # Lua script: https://github.com/scrapy-plugins/scrapy-splash
        script = """
        function main(splash)
        assert(splash:go(splash.args.url))
        assert(splash:wait(0.5))
        button = splash:select("li[class=next] a")
        splash:set_viewport_full()
        splash:wait(0.1)
        button:mouse_click()
        splash:wait(1.0)
        return { url = splash:url(), html = splash:html() } 
        end
        """

        yield SplashRequest(url = response.url,
                            callback = self.parse,
                            endpoint='execute', #the script
                            args={'lua_source' : script})
