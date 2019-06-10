# -*- coding: utf-8 -*-
from scrapy.loader import ItemLoader
from amazonScraper.items import AmazonscraperItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class Spider01Spider(CrawlSpider):
    name = 'spider01'
    allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.com/dp/b017l376au']
    rules = [
        Rule(LinkExtractor(allow=r"(?:\/dp\/)|(?:\/gp\/product\/)"), callback='parse_items', follow=True),
             Rule(LinkExtractor(unique=True, canonicalize=True)),
    ]

    def getPrice(self, response):
        if self.site == 'amazon':
            return response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()


    def getImg(self, response):
        if self.site == 'amazon':
            return response.xpath('//*[@id="landingImage"]/@data-old-hires').extract_first()

    def parse_items(self, response):
        item = ItemLoader(item=AmazonscraperItem(), response=response)
        item.add_value('title', response.xpath('//head/title/text()').extract_first())
        item.add_value('price', self.getPrice(response))
        item.add_value('image_urls', self.getImg(response))
        item.add_value('product_desc', response.xpath('//meta[contains(@name, "description")]/@content').extract_first())
        return item.load_item()

    def __init__(self, output='', site='',*args, **kwargs):
        self.output = output
        self.site = site
        super(Spider01Spider, self).__init__(*args, **kwargs)
