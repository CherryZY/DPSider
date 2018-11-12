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
    __items = {}
    __items_classify = []
    __items_areas = []

    def __init__(self):
        self.__f = FileIO(fileConfig['classFile'])

    def __del__(self):
        self.__items['shop_classify'] = self.__items_classify
        self.__items['shop_area'] = self.__items_areas
        # self.__f.write(self.__items)

    def process_item(self, item, spider):
        logging.debug("[DPSider.pipelines.DpsiderPipeline] in param:{%s,%s}", item, spider)
        # if item['type'] == 'classify':
        #     self.__items_classify.append(item)
        # elif item['type'] == 'area':
        #     self.__items_areas.append(item)
