# encoding: utf-8
'''
@author: yue.zhang
@project: 
@time: 2018/11/12 11:22
@desc:
'''

import threading
from scrapy.cmdline import execute


if __name__ == '__main__':
    # execute(['scrapy', 'crawl', 'classify_list'])
    # execute(['scrapy', 'crawl', 'shop_list'])
    execute(['scrapy', 'crawl', 'shop_detail'])






