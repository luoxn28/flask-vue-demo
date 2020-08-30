'''excel读操作组件'''
import os

import xlrd

XLSX = 'xlsx'
XLS = 'xls'


# 判断excel文件名是否合法
def excel_name_legal(filename):
    filename = os.path.basename(filename)
    return filename and ('.' in filename) and (filename.rsplit('.', 1)[1] in (XLSX, XLS))


# 获取excel类型
def excel_file_type(filename):
    filename = os.path.basename(filename)
    return filename.rsplit('.', 1)[1]


# 读取sheet列表
def read_sheet_names(filepath):
    workbook = xlrd.open_workbook(filepath)
    return workbook.sheet_names()


if __name__ == '__main__':
    print(os.path.basename('/Users/luoxiangnan/PycharmProjects/flask-vue-demo/dist/frontend/static/名单3.xls'))
    print(os.path.basename('名单3.xls'))
