# -*- coding: utf-8 -*-
"""
sudo docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash --max-timeout 36
scrapy crawl cars -o cars.csv
"""
import scrapy
from scrapy.http import Request
from scrapy_splash import SplashRequest


class CarsSpider(scrapy.Spider):
    name = 'cars'
    allowed_domains = ['baierl.com'] #get rid of http://www. and traling /
    start_urls = ['https://www.baierl.com/new-inventory/']

    def get_filter_script(self): #returns html
        return """
function main(splash)
    assert(splash:go(splash.args.url))
    splash:wait(5)

    local get_element_dim_by_xpath = splash:jsfunc([[
        function(xpath) {
            var element = document.evaluate(xpath, document, null,
                XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            var element_rect = element.getClientRects()[0];
            return {"x": element_rect.left, "y": element_rect.top}
        }
    ]])

    -- -- Find the YEAR drop down
    local year_drop_dimensions = get_element_dim_by_xpath(
        '//h2[contains(@class, "label ") and contains(text(), "Year ")]')
    splash:set_viewport_full()
    splash:mouse_click(year_drop_dimensions.x, year_drop_dimensions.y)
    splash:wait(1.5)

    -- -- Clicks the 202X year
    local year_dimensions = get_element_dim_by_xpath(
        '//li[contains(@data-value, "2020")]/span')
    splash:set_viewport_full()
    splash:mouse_click(year_dimensions.x, year_dimensions.y)
    splash:wait(5)

    -- Find the MAKE drop down
    local make_drop_dimensions = get_element_dim_by_xpath(
        '//h2[contains(@class, "label ") and contains(text(), "Make ")]')
    splash:set_viewport_full()
    splash:mouse_click(make_drop_dimensions.x, make_drop_dimensions.y)
    splash:wait(1.5)

    -- Clicks the Toyota make
    local make_dimensions = get_element_dim_by_xpath(
        '//li[contains(@data-filters, "make_toyota")]/span')
    splash:set_viewport_full()
    splash:mouse_click(make_dimensions.x, make_dimensions.y)
    splash:wait(5)

    return splash:html()
end 
        """

    def get_script_at_first_page(self): #similar to above, returns html and url
        return """
function main(splash)
    assert(splash:go(splash.args.url))
    splash:wait(5)

    local get_element_dim_by_xpath = splash:jsfunc([[
        function(xpath) {
            var element = document.evaluate(xpath, document, null,
                XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            var element_rect = element.getClientRects()[0];
            return {"x": element_rect.left, "y": element_rect.top}
        }
    ]])

    -- -- Find the YEAR drop down
    local year_drop_dimensions = get_element_dim_by_xpath(
        '//h2[contains(@class, "label ") and contains(text(), "Year ")]')
    splash:set_viewport_full()
    splash:mouse_click(year_drop_dimensions.x, year_drop_dimensions.y)
    splash:wait(1.5)

    -- -- Clicks the 202X year
    local year_dimensions = get_element_dim_by_xpath(
        '//li[contains(@data-value, "2020")]/span')
    splash:set_viewport_full()
    splash:mouse_click(year_dimensions.x, year_dimensions.y)
    splash:wait(5)

    -- Find the MAKE drop down
    local make_drop_dimensions = get_element_dim_by_xpath(
        '//h2[contains(@class, "label ") and contains(text(), "Make ")]')
    splash:set_viewport_full()
    splash:mouse_click(make_drop_dimensions.x, make_drop_dimensions.y)
    splash:wait(1.5)

    -- Clicks the Toyota make
    local make_dimensions = get_element_dim_by_xpath(
        '//li[contains(@data-filters, "make_toyota")]/span')
    splash:set_viewport_full()
    splash:mouse_click(make_dimensions.x, make_dimensions.y)
    splash:wait(5)

    -- finds next page and clicks, returns url & html of next page
    next_button = splash:select("*[class='page-next ']")
    next_button.mouse_click()
    splash:wait(4)
    return {
        url = splash:url(),
        html = splash:html()
    }
end        
        """

    def get_script_at_next_page(self):
        return """
        function main(splash)
        assert(splash:go(splash.args.url))
        splash:wait(5)
        
        next_button = splash:select("*[class='page-next ']")
        next_button.mouse_click()
        splash:wait(4)
        return {
        url = splash:url(),
        html = splash:html()
        }
        end
        """
    

    def start_requests(self):
        filters_script = self.get_filter_script()

        for url in self.start_urls:
            yield SplashRequest(url = url,
                                callback = self.parse,
                                endpoint = 'execute',
                                args = {'lua_source' : filters_script } )

    def parse(self, response):

        cars_urls = response.xpath('//*[@class="title"]/a/@href').extract()
        for url in cars_urls:
            abs_url = response.urljoin(url)
            yield Request(url = abs_url,
                          callback = self.parse_car)

        script_at_first_page = self.get_script_at_first_page()
        script_at_next_page = self.get_script_at_next_page()
        script = None
        if response.url is self.start_urls[0]:
            script = script_at_first_page
        else:
            script = script_at_next_page

        yield SplashRequest(url = response.url,
                            callback = self.parse,
                            endpoint = 'execute',
                            args = {'lua_source' : script } )
        
    def parse_car(self, response):
        #name can be in different parts
        name = ''.join(response.xpath('//h1//text()').extract() )
        price = response.xpath('//*[@class="finalPrice"]/span/text()').extract_first()
        stock = response.xpath('//li[@class="stock"]/span[@class="value"]/text()').extract_first()

        yield { 'name' : name,
                'price' : price,
                'stock' : stock }

    
