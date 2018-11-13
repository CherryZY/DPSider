# -*- coding: utf-8 -*-
import scrapy
import ast
from DPSider.configs import logging, fileConfig, url_prefix
from DPSider.utils.fileio import FileIO
import re

'''
读取商铺列表信息-路径: shopList.json文件，获取要爬取的店铺详情链接
'''
def read_shop_list():
    f = FileIO(fileConfig['listFile'])
    result = f.read()
    logging.debug("[read_shop_list] read info :%s" % result)
    if not result and result == '':
        return []
    classifyUrlList = []
    type(result)
    for it in result:
        classifyUrlList.append(it["shopPath"])
    return classifyUrlList

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
店铺详情html解析爬取
'''
class ShopDetailSpider(scrapy.Spider):
    name = 'shop_detail'
    allowed_domains = ['dianping.com']
    start_urls = ["https://www.dianping.com/shop/102457506"]

    # def start_requests(self):
    #     pages = []
    #     classifyItems = read_shop_list()
    #     if not classifyItems:
    #         return
    #     for url in classifyItems:
    #         page = scrapy.Request(url_prefix + url)
    #         pages.append(page)
    #     return pages

    def parse(self, response):
        logging.debug(response)
        result = response.xpath('//div[@id="main-body"]/div[@class="shop-wrap"]')
        shopImgs = result.xpath('./div[@class="shop-main clearfix"]/div[@class="slider-wrapper J_wrapPic"]/div[@class="slider"]/img')
        # 店铺主图（大图）
        shopMainImgs = []
        for img in shopImgs:
            try:
                shopMainImgs.append(url_prefix + img.xpath('./@src').extract()[0].strip("//"))
            except Exception as e:
                logging.info("[DPSider.spiders.shop_detail.ShopDetailSpider#parse] parse img info:{%s}",e)
                continue
        # 店铺主图的导航图（小图）
        # shopNavImgs = []
        # sliderNavImgs = result.xpath('./div[@class="shop-main clearfix"]/div[@class="slider-wrapper J_wrapPic"]/div[@class="slider-nav"]/span')
        # logging.debug("================" + str(sliderNavImgs.extract()))
        # for sliderNavImg in sliderNavImgs:
        #     logging.debug("================" + sliderNavImg)
        #     try:
        #         shopNavImgs.append(sliderNavImg.xpath('./img/@src').extract_first().strip("//"))
        #     except Exception as e:
        #         logging.info("[DPSider.spiders.shop_detail.ShopDetailSpider#parse] parse NavImg info:{%s}",e)
        #         continue

        # 店铺基本信息
        shopBasicInfo = result.xpath('./div[@class="shop-main clearfix"]/div[@class="shop-brief"]/div[@id="J_boxDetail"]/div[@class="shop-info"]')
        shopName = shopBasicInfo.xpath('./div[@class="shop-name"]/h1/text()').extract_first()
        shopStar = shopBasicInfo.xpath('./div[@class="comment-rst"]/span/@class').extract()
        commentCount = shopBasicInfo.xpath('./div[@class="comment-rst"]/a/text()').extract()
        shopStar = re.search("[0-9]{2}", shopStar[0]).group()
        commentCount = re.search("[0-9]+", commentCount[0]).group()
        shopAddress = shopBasicInfo.xpath('./p[@class="shop-contact address"]/span/@title').extract_first()
        shopOfficeHours = shopBasicInfo.xpath('./p[@class="shop-contact"]/text()').extract_first()
        shopOfficeHours = shopOfficeHours.strip().strip('\n')
        shopPhoneNum = shopBasicInfo.xpath('./div[@class="shop-contact telAndQQ"]/span/strong/text()').extract()
        shopGifts = result.xpath('./div[@class="shop-main clearfix"]/div[@class="shop-brief"]/div[@class="shop-gifts clearfix"]/div/span/text()').extract_first()
        # TODO：团购券信息
        # 店铺详情图片
        shopDetialImgsUrl = []
        shopDetailUrls = []
        shopDetailImgs = response.xpath('//div[@class="feat-slide"]/div[@class="slider-box J_wrapPic"]/ul/li')
        for img in shopDetailImgs:
            path = img.xpath('/@href').extract()
            imgurl = img.xpath('/@src').extract()
            shopDetialImgsUrl.append(url_prefix + imgurl.strip('//'))
            shopDetailUrls.append(path)

        logging.debug('"shopImgs":%s,"shopName":%s,"shopStar":%s,"commentCount":%s,"address":%s,"officeHour":%s,"gifts":%s,"phoneNum":%s,"shopDetailUrls":%s, shopDetialImgsUrl:%s' %
                      (shopMainImgs, shopName, shopStar, commentCount, shopAddress, shopOfficeHours, shopGifts, shopPhoneNum, shopDetailUrls, shopDetialImgsUrl))

        pass
