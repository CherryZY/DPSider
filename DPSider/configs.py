# encoding: utf-8
'''
@author: yue.zhang
@project: 
@time: 2018/11/12 14:07
@desc:
'''
import logging

# url前缀
url_prefix = "http://"
url_ssl_prefix = "https://"
url_dian_ping_prefix = "https://www.dianping.com"

# 文件配置
fileConfig = {
    "ips" : "C:\\Users\\YUE.ZHANG\\Desktop\\DPSider\\DPSider\\ips.json",
    "classFile" : "C:\\Users\\YUE.ZHANG\\Desktop\\DPSider\\DPSider\\class.json",
    "listFile" : "C:\\Users\\YUE.ZHANG\\Desktop\\DPSider\\DPSider\\shopList.json",
    "detailFile" : "C:\\Users\\YUE.ZHANG\\Desktop\\DPSider\\DPSider\\shopDetialList.json",
    "exportLocation" : "C:\\Users\\YUE.ZHANG\\Desktop\\DPSider\\DPSider\\exportShopList.excel"
}

# 日志配置
logConfig = {
    "filename":  'C:\\Users\\YUE.ZHANG\\Desktop\\DPSider\\DPSider\\dpSpider_log.log',
    "filemode": 'w',
    "format": "%(message)s"
}
logging.basicConfig(**logConfig)

if __name__ == '__main__':
    # print(os.path)
    pass
