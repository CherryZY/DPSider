# encoding: utf-8
'''
@author: yue.zhang
@project: DPSider-master
@time: 2018/11/12 16:45
@desc: fileio.py
'''
import json
import logging
from DPSider.enum.filereadenum import FileReadWayEnum
from DPSider.configs import fileConfig
import ast
import re

import os, sys

'''
文件io操作
'''
class FileIO:

    __file = None
    __formate = False

    '''
    r+ : 可读写
    w+ : 可读写两种操作（会首先自动清空文件内容）
    a+ : 追加读写
    r : 读取 
    w : 写入 
    a : 追加
    '''
    def __init__(self, fileName, operation="r+", formate=False):
        self.__formate = formate
        self.__file = open(fileName, operation)

    def read(self, limit=1, readWay=FileReadWayEnum.READ_ALL):
        if readWay == FileReadWayEnum.READ_ALL:
            strs = self.__file.read()
            return str(strs)
        elif readWay == FileReadWayEnum.READ_LINE:
            return str(self.__file.readline(limit))
        elif readWay == FileReadWayEnum.READ_LINES:
            return str(self.__file.readlines())

    def load(self):
        return json.load(self.__file)

    def write(self, content):
        logging.debug("[DPSider.utils.fileio.FileIO#write] in param{%s}", content)
        strItems = str(content)
        strItems = strItems.replace('\'', '\"')
        if self.__formate:
            strItems = json.dumps(strItems)
        self.__file.write(strItems)


    def __del__(self):
        self.__file.close()
