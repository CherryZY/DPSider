# encoding: utf-8
'''
@author: yue.zhang
@project: DPSider
@time: 2018/11/14 10:01
@desc: command.py
'''
from scrapy.command import ScrapyCommand
from scrapy.crawler import Crawler


class command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        pass
        # settings = get_project_settings()

        # for spider_name in self.crawler.spiders.list():
        #     crawler = Crawler(settings)
        #     crawler.configure()
        #     spider = crawler.spiders.create(spider_name)
        #     crawler.crawl(spider)
        #     crawler.start()
        #
        # self.crawler.start()