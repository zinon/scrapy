import scrapy
"""
run: scrapy runspider quotes_standalone/quotes_standalone.py -o quotes.csv
"""
class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com'] #Attention: remove trailing / from domains
    start_urls = ['http://quotes.toscrape.com/']
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
