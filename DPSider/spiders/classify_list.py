# -*- coding: utf-8 -*-
import scrapy
from DPSider.configs import logging
from DPSider.items import BaseItem, ShopListItem


'''
解析“大众点评”建材页面的分类（建材商家类别、区域）
'''
class ClassifyListSpider(scrapy.Spider):

    name = 'classify_list'
    allowed_domains = ['dianping.com']
    start_urls = ['http://www.dianping.com/shenzhen/ch90']

    def __base_parse(self, itemIn):
        item = BaseItem()
        item['name'] = itemIn.xpath('./a/text()').extract()[0].strip('\n').strip()
        item['url'] = itemIn.xpath('./a/@href').extract()[0].strip('//')
        return item

    def parse(self, response):
        for i in range(1, 3):
            content = response.xpath('//div[@class="shopsearch"]/div[@class="type"][' + str(i) +']')
            result = content.xpath('./div/ul/li')
            for classify in result:
                classifyItem = self.__base_parse(classify)
                # 类型为"分类名"
                if i == 1:
                    classifyItem['type'] = "classify"
                # 类型为"区域名"
                elif i == 2 :
                    classifyItem['type'] = "area"
                yield classifyItem
