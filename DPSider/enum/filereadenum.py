# encoding: utf-8
'''
@author: yue.zhang
@project: DPSider-master
@time: 2018/11/12 17:22
@desc: filereadenum.py
'''
from enum import Enum

'''
文件读取方式
'''
class FileReadWayEnum(Enum):
    READ_ALL = 0
    READ_LINE = 1
    READ_LINES = 2