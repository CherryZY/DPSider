# encoding: utf-8
'''
@author: yue.zhang
@project: DPSider
@time: 2018/11/14 17:09
@desc: shop_list_h5.py
'''
import scrapy


class ShopListH5(scrapy.Spider):
    name = 'shop_list_h5'
    allowed_domains = ['dianping.com']
    start_urls = ['http://www.dianping.com/shop/82523000']

    def parse(self, response):
        pass