# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from DPSider.configs import fileConfig, logging
from DPSider.utils.fileio import FileIO

# item输出管道
class DpsiderPipeline(object):

    __f = None
    __spider = ""
    __items = {}
    __items_classify = []
    __items_areas = []

    # 店铺列表页
    __items_shop_list = []
    # 店铺详情页
    __items_shop_detail = []

    def __init__(self):
        pass

    def __del__(self):
        pass

    def process_item(self, item, spider):
        self.__spider = spider.name
        # logging.debug("[DPSider.pipelines.DpsiderPipeline] in param:{%s}", item)
        if spider.name == 'classify_list':
            if item['type'] == 'classify':
                self.__items_classify.append(item)
            elif item['type'] == 'area':
                self.__items_areas.append(item)
        elif spider.name == 'shop_list':
            self.__items_shop_list.append(item)
        elif spider.name == 'shop_detail':
            self.__items_shop_detail.append(item)


    def open_spider(self, spider):
        self.__spider = spider.name
        if self.__spider == "classify_list":
            self.__f = FileIO(fileConfig['classFile'], "w+", True)
        elif self.__spider == "shop_list":
            self.__f = FileIO(fileConfig['listFile'], "w+", True)
        elif self.__spider == "shop_detail":
            self.__f = FileIO(fileConfig['detailFile'], "r+")

    def close_spider(self, spider):
        if self.__items_classify and self.__items_areas and len(self.__items_classify) > 0:
            self.__items['shop_classify'] = self.__items_classify
            self.__items['shop_area'] = self.__items_areas
            self.__f.write(self.__items)
        if self.__items_shop_list and len(self.__items_shop_list) > 0:
            logging.debug(self.__items_shop_list)
            self.__f.write(self.__items_shop_list)
        if self.__items_shop_detail and len(self.__items_shop_detail) > 0:
            logging.debug(self.__items_shop_detail)
            # self.__f.write(self.__items_shop_detail)
