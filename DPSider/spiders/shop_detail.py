# -*- coding: utf-8 -*-
import scrapy
import ast
from DPSider.configs import logging, fileConfig, url_prefix, USER_AGENT
from DPSider.utils.fileio import FileIO
import re
import random
from DPSider.items import ShopDetail


'''
读取商铺列表信息-路径: shopList.json文件，获取要爬取的店铺详情链接
'''
def read_shop_list():
    f = FileIO(fileConfig['listFile'])
    result = f.load()
    if not result and result == '':
        return []
    type(result)
    resultArray = ast.literal_eval(result)
    return resultArray


'''
解析团购券信息
'''
def parse_group_coupon(result):
    groupBuyCouponsInfo = []
    groupBuyCoupons = result.xpath('./div[@class="shop-profits clearfix J-fold"]/ul/li')
    for groupBuyCoupon in groupBuyCoupons:
        g = {}
        g['imgUrl'] = groupBuyCoupon.xpath('./a/div[@class="img-wrap"]/img/@src').extract()
        g['info'] = groupBuyCoupon.xpath('./a/div[@class="text-wrap"]/p/text()').extract()
        priceInfo = groupBuyCoupon.xpath('./a/div[@class="text-wrap"]/div[@class="price"]')
        g['currentPrice'] = priceInfo.xpath('./em/text()').extract()
        g['lastPrice'] = priceInfo.xpath('./span[1]/text()').extract()
        g['discount'] = priceInfo.xpath('./i/text()').extract()
        g['soldCount'] = priceInfo.xpath('./span[@class="sales"]/text()').extract()
        groupBuyCouponsInfo.append(g)
    return groupBuyCouponsInfo


'''
初始化店铺map
'''
def get_shop_path_map(shop_arr):
    shop_path_map = {}
    if not shop_arr and len(shop_arr) < 1:
        return None
    for shop in shop_arr:
        if shop and shop["shopPath"] :
            shop_path_map[shop["shopPath"]] = shop
    return shop_path_map

'''
店铺详情html解析爬取
'''
class ShopDetailSpider(scrapy.Spider):

    __shopMap = {}
    name = 'shop_detail'
    allowed_domains = ['dianping.com']
    start_urls = ['http://www.dianping.com/shop/82523000']

    # 预定义start_urls
    def start_requests(self):
        url_list = []
        shop_list = read_shop_list()
        self.__shopMap = get_shop_path_map(shop_list)
        if self.__shopMap:
            for (k, v) in self.__shopMap.items():
                url_list.append(k)
        pages = []
        if not url_list or len(url_list) < 1:
            page = scrapy.Request("https://www.dianping.com/shop/102457506")
            pages.append(page)
            return pages
        logging.debug("request urls:{%s}" % url_list)
        userAgent = random.choice(USER_AGENT)
        for url in url_list:
            if not url.startswith("http://") and not url.startswith("https://"):
                url = url_prefix + url
            page = scrapy.Request(userAgent, url)
            pages.append(page)
        return pages

    def parse(self, response):
        shopDetailItem = ShopDetail()
        logging.debug(response.request.url)
        logging.debug(response.status)
        if response.request.url.startswith("https://verify.meituan.com/") or response.status == 403:
            raise Exception("爬取次数过多，ban....")
        shopBasicListInfo = self.__shopMap[response.request.url]
        logging.debug(shopBasicListInfo)
        result = response.xpath('//div[@id="main-body"]/div[@class="shop-wrap"]')
        # 从request后缀获取
        shopId = shopBasicListInfo["shopId"]
        shopImgs = result.xpath('./div[@class="shop-main clearfix"]/div[@class="slider-wrapper J_wrapPic"]/div[@class="slider"]/img')
        shopMainImgs = []
        for img in shopImgs:
            try:
                shopMainImgs.append(url_prefix + img.xpath('./@src').extract()[0].strip("//"))
            except Exception as e:
                logging.info("[DPSider.spiders.shop_detail.ShopDetailSpider#parse] parse img info:{%s}", e)
                continue
        shopBasicInfo = result.xpath(
            './div[@class="shop-main clearfix"]/div[@class="shop-brief"]/div[@id="J_boxDetail"]/div[@class="shop-info"]')
        shopName = shopBasicInfo.xpath('./div[@class="shop-name"]/h1/text()').extract_first()
        shopStar = shopBasicInfo.xpath('./div[@class="comment-rst"]/span/@class').extract_first()
        # commentCount = shopBasicInfo.xpath('./div[@class="comment-rst"]/a/text()').extract()
        shopStar = re.search("[0-9]{1,2}", shopStar).group()
        shopAddress = shopBasicInfo.xpath('./p[@class="shop-contact address"]/span/@title').extract_first()
        shopOfficeHours = shopBasicInfo.xpath('./p[@class="shop-contact"]/text()').extract_first()
        if shopOfficeHours:
            shopOfficeHours = shopOfficeHours.strip().replace('\n', " ")
        shopPhoneNum = shopBasicInfo.xpath('./div[@class="shop-contact telAndQQ"]/span/strong/text()').extract()
        shopGifts = result.xpath(
            './div[@class="shop-main clearfix"]/div[@class="shop-brief"]/div[@class="shop-gifts clearfix"]/div/span/text()').extract_first()
        shopDetailImgsUrl = []
        shopDetailUrls = []
        shopDetailImgPath_1 = response.xpath('//div[@class="slider-box J_wrapPic"]/ul/li/a/@href').extract_first()
        shopDetailImgUrl_1 = response.xpath('//div[@class="slider-box J_wrapPic"]/ul/li/a/img/@src').extract_first()
        shopLocationXPath = response.xpath('//div[@class="shop-location"]/span')
        shopLocation = []
        if shopLocationXPath and len(shopLocationXPath) > 0:
            for sl in shopLocationXPath:
                shopLocation.append(sl.xpath('./text()'))

        shopDetailItem['shopId'] = shopId
        shopDetailItem['shopMainImgs'] = shopMainImgs
        shopDetailItem['shopName'] = shopName
        shopDetailItem['shopStar'] = shopStar
        shopDetailItem['shopAddress'] = shopAddress
        shopDetailItem['shopOfficeHours'] = shopOfficeHours
        if shopPhoneNum and len(shopPhoneNum) > 0:
            shopDetailItem['shopPhoneNum'] = shopPhoneNum[0]
        shopDetailItem['shopGift'] = shopGifts
        # shopDetailItem['shopLocation'] = shopBasicListInfo['shopLocation']
        shopDetailItem['shopInfoText'] = shopBasicListInfo['shopInfoText']

        if shopDetailImgPath_1 and shopDetailImgUrl_1:
            shopDetailImgUrl_1 = url_prefix + shopDetailImgUrl_1.strip('//')
            shopDetailImgsUrl.append(shopDetailImgUrl_1)
            shopDetailUrls.append(shopDetailImgPath_1)
            shopDetailImgs = response.xpath('//div[@class="slider-box J_wrapPic"]/textarea[@class="Hide"]/li')
            for img in shopDetailImgs:
                path = img.xpath('./a/@href').extract_first()
                imgurl = img.xpath('./a/img/@src').extract_first()
                shopDetailImgsUrl.append(url_prefix + imgurl.strip('//'))
                shopDetailUrls.append(path)

            shopDetailItem['shopDetailImgs'] = shopDetailImgsUrl
            shopDetailItem['shopDetailUrls'] = shopDetailUrls

        logging.debug(shopDetailItem)
        yield shopDetailItem
