#!/usr/bin/env python
# encoding: utf-8
'''
@author: yue.zhang
@project: DPSpider
@file: middlewares.py
@time: 2018/11/11 21:06
@desc:
'''

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random


# 店铺详情spider中间件
class ShopDetailSpiderMiddleware(UserAgentMiddleware):

    '''
        访问相关配置信息
    '''
    @classmethod
    def from_crawler(cls, crawler):
        s = cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.
        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.
        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.
        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
