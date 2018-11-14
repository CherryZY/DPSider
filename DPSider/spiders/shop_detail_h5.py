# encoding: utf-8
'''
@author: yue.zhang
@project: DPSider
@time: 2018/11/14 17:10
@desc: shop_detail_h5.py
'''
import scrapy


class ShopDetailH5(scrapy.Spider):
    name = 'shop_detail_h5'
    allowed_domains = ['dianping.com']
    start_urls = ['http://www.dianping.com/shop/82523000']



