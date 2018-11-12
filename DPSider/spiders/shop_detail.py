# -*- coding: utf-8 -*-
import scrapy


class ShopDetailSpider(scrapy.Spider):
    name = 'shop_detail'
    allowed_domains = ['dianping.com']
    start_urls = ['http://dianping.com/']

    def parse(self, response):
        pass
