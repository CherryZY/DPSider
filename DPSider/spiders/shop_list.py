# -*- coding: utf-8 -*-
import scrapy
from DPSider.items import ShopListItem
from DPSider.utils.fileio import FileIO
from DPSider.configs import fileConfig, logging, url_prefix, url_dian_ping_prefix
import ast
import re

'''
读取商铺分类信息: 读取class.json文件，获取要爬取的类目
'''
def read_classify_list():
    f = FileIO(fileConfig['classFile'])
    result = f.read()
    logging.debug(result)
    if not result and result == '':
        return []
    classifyUrlList = []
    dictResult = ast.literal_eval(result)
    for it in dictResult["shop_classify"]:
        classifyUrlList.append(it["url"])
    return classifyUrlList


'''
店铺列表
'''
class ShopListSpider(scrapy.Spider):
    name = 'shop_list'
    allowed_domains = ['dianping.com']
    start_urls = ['http://dianping.com/']

    def start_requests(self):
        pages = []
        classifyItems = read_classify_list()
        if not classifyItems:
            return
        for url in classifyItems:
            page = scrapy.Request(url_prefix + url)
            pages.append(page)
        return pages


    def parse(self, response):
        if not response:
            return
        results = response.xpath('//div[@class="shop-list"]/li')
        for result in results:
            logging.debug("====================================================================")
            shopMainInfo = result.xpath('./div[@class="shop-info shop-info_materials"]')
            # 店铺图片url
            picUrl = result.xpath('./a/img/@src').extract()
            # 店铺路径
            shopPath = result.xpath('./a/@href').extract()[0].strip('//')
            # 店铺id
            shopId = result.xpath('./@data-id').extract()[0].strip()
            # 店铺名称
            shopName = shopMainInfo.xpath('./div[@class="shop-main"]/div[@class="shop-title"]/h3/a/text()').extract()
            # 店铺服务及区域信息
            shopInfoText = shopMainInfo.xpath('./div[@class="shop-main"]/div[@class="shop-info-text-i"]/span')
            shopInfoTextList = []
            for shopInfo in shopInfoText:
                shopInfoTextList.append(shopInfo.xpath('./text()').extract()[0])
            commentCount = ''
            starCount = ''
            # 团购url
            groupBuyTextUrl = shopMainInfo.xpath('./div[@class="shop-sales-promotion clearfix"]/a/@href').extract()
            # 团购信息
            groupBuyText = shopMainInfo.xpath('./div[@class="shop-sales-promotion clearfix"]/a/p').extract()
            comment = shopMainInfo.xpath('./div[@class="shop-main"]/div[@class="user-comment"]')
            comment_star = comment.xpath('./span/@class').extract()
            if comment_star and len(comment_star) > 0:
                starCount = re.search("[0-9]", comment_star[0]).group()
            comment_count = comment.xpath('./a/text()').extract()
            if comment_count and len(comment_count) > 0:
                commentCount = re.search("[0-9]", comment_count[0]).group()
            shopListItem = ShopListItem()
            shopListItem['shopId'] = shopId
            if shopName and len(shopName) > 0:
                shopListItem['name'] = shopName[0]
            shopListItem['shopPath'] = url_prefix + shopPath.strip()
            if picUrl and len(picUrl) > 0:
                shopListItem['picUrl'] = url_prefix + picUrl[0].strip('//')
            shopListItem['shopInfoText'] = shopInfoTextList
            if groupBuyText and len(groupBuyText) > 0:
                for index in range(len(groupBuyText)):
                    groupBuyText[index] = groupBuyText[index].strip().strip('<p>').strip('</p>').strip('<em>').strip('</em>')
            shopListItem['groupBuyText'] = groupBuyText
            if groupBuyTextUrl and len(groupBuyTextUrl) > 0:
                for index in range(len(groupBuyTextUrl)):
                    groupBuyTextUrl[index] = groupBuyTextUrl[index].strip().strip('//')
            shopListItem['groupBuyUrl'] = groupBuyTextUrl
            shopListItem['commentCount'] = commentCount
            shopListItem['starCount'] = starCount
            logging.debug("====================================================================")
            yield shopListItem
        # 递归遍历下一页
        page_urls = response.xpath('.//div[@class="pages"]/a[@title="下一页"]/@href')
        suffix_url = page_urls.extract()[0]
        yield scrapy.Request(url_dian_ping_prefix + suffix_url, callback=self.parse)





