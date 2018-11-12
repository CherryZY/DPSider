# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


'''
分类item
'''
class BaseItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    pass

'''
店铺list item
'''
class ShopListItem(scrapy.Item):
    # 店铺id
    shopId = scrapy.Field()
    # 店铺名称
    name = scrapy.Field()
    # 店铺path
    shopPath = scrapy.Field()
    # 图片path
    picUrl = scrapy.Field()
    # 店铺信息
    shopInfoText = scrapy.Field()
    # 团购信息
    groupBuyText = scrapy.Field()
    # 团购信息url
    groupBuyUrl = scrapy.Field()
    # 点评数量
    commentCount = scrapy.Field()
    # 星级
    starCount = scrapy.Field()
    pass



class DpsiderItem(scrapy.Item):
    pass
