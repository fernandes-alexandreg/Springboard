import scrapy


class QuotesSpider_Dictionary_xpath(scrapy.Spider):
    name = "quotes_dict_xpath"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('span[@class="text"]/text()').extract(),
                'author': quote.xpath('span/small[@class="author"]/text()').extract(),
                'tags': quote.xpath('div[@class="tags"]/a[@class="tag"]/text()').extract(),
            }


class QuotesSpider_Pages_xpath(scrapy.Spider):
    name = "quotes_pages_xpath"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('span[@class="text"]/text()').extract(),
                'author': quote.xpath('span/small[@class="author"]/text()').extract(),
                'tags': quote.xpath('div[@class="tags"]/a[@class="tag"]/text()').extract(),
            }

        next_page = response.xpath('//a[contains(text(),"Next")]/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class QuotesSpider_Project_xpath(scrapy.Spider):
    name = "toscrape-xpath"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.xpath('//a[contains(text(),"Next")]/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

