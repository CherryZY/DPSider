# encoding: utf-8
'''
@author: yue.zhang
@project: DPSider
@time: 2018/11/13 10:26
@desc: excelio.py
'''

import xlwt
from DPSider.configs import fileConfig
from datetime import datetime

def getCurrentDate():
    today = datetime.today()
    today_date = datetime.date(today)
    return today_date

'''
 将数据写入并生成 fileName 的文件
'''
def writeDataToExcel(fileName, result, addTimeSuffix = True):
    wbk = xlwt.Workbook()
    # 新建一个名为Sheet1的excel sheet.cell_overwrite_ok = True是为了能对同一个单元格重复操作。
    sheet = wbk.add_sheet('Sheet1',cell_overwrite_ok=True)
    # 遍历result中的每个元素。
    for i in range(len(result)):
        for j in range(len(result[i])):
            sheet.write(i,j,result[i][j])
    if addTimeSuffix == True:
        fileName += str(getCurrentDate())
    wbk.save(fileConfig['exportLocation'] + fileName + '.xls')
