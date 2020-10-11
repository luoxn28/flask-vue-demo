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


# excel文件是否包含该sheet
def contains_sheet(filepath, sheet):
    return sheet and sheet in read_sheet_names(filepath)


# 如果sheet为空则取第一个sheet
def default_if_null(workbook, sheet):
    if sheet is None:
        sheet = workbook.sheet_names()[0]
    return sheet


if __name__ == '__main__':
    print(os.path.basename('/Users/luoxiangnan/PycharmProjects/flask-vue-demo/dist/frontend/static/名单3.xls'))
    print(os.path.basename('名单3.xls'))
