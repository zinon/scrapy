# -*- coding: utf-8 -*-
import scrapy

class QuotesSpider(scrapy.Spider):
    """
    execute: scrapy crawl quotes -o items.csv or .json
    view: python3 -m json.tool items.json
    """
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com'] #Attention: remove trailing / from domains
    start_urls = ['http://quotes.toscrape.com/']

    def parse_(self, response):
        """
        gets right-hand side tags and adds them in scrapy.Item
        """
        h1_tag = response.xpath('//h1/a/text()').extract_first()
        tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()

        
        
    def parse(self, response):
        """
        reads off quoted text from each quote class
        """
        quotes = response.xpath('//*[@class="quote"]')
        for quote in quotes:

            ### quotes
            
            # quote via class=text
            text =  quote.xpath('.//*[@class="text"]/text()').extract_first() 

            # quote via itemprop=text
            #text =  quote.xpath('.//*[@itemprop="text"]/text()').extract_first()

            ### author
            author = quote.xpath('.//*[@itemprop="author"]/text()').extract_first()

            ### quote tags 

            #via content (note syntax @content)
            #tags = quote.xpath('.//*[@itemprop="keywords"]/@content').extract_first().split(',')

            #via class=tag
            tags = quote.xpath('.//*[@class="tag"]/text()').extract()

            yield { "text" : text,
                    "author" : author,
                    "tags" : tags }

            #navigate over linked "next" pages
        next_page_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        print("NEXT", next_page_url, absolute_next_page_url)
        yield scrapy.Request(url = absolute_next_page_url, callback=self.parse)
        

        #if not in the "parse" function need to add
        # ..., callback=self.parse_page)
        
    #def parse(self, response):
    #    #self.simple(response)
   #     yield self.complex(response)

#Notes:
#----------------------------------------------------------------
# get selector and extract: 
# quote.xpath('.//*[@class="text"]').extract()
# human readable:
# quote.xpath('.//*[@class="text"]/text()').extract_first()
#
# or
#
# quote.xpath('.//*[@itemprop="text"]/text()').extract_first()
#----------------------------------------------------------------
# The . selects only from the content of the custom selector
# whithout . we select all, similar to reading off from response
#
# response.xpath('//*[@class="text"]/text()')
#----------------------------------------------------------------
# obtain all class=next
# enter element "a"
# access href

