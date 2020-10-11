'''excel(xlsx文件格式)读操作组件'''

import xlrd

from backend.component.excel.base import excelr
from backend.component.excel.base.excelr import read_sheet_names


# 读取sheet合并单元格信息，结果格式为: [(左上角行, 右下角行, 左上角列, 右下角列)]
def read_sheet_merged_cells(filepath, sheet=None):
    workbook = xlrd.open_workbook(filepath)
    sheet = excelr.default_if_null(workbook, sheet)
    worksheet = workbook.sheet_by_name(sheet)
    return worksheet.merged_cells


# 读取某个sheet所有文本内容
def read_excel_data(filepath, sheet=None):
    workbook = xlrd.open_workbook(filepath)
    sheet = excelr.default_if_null(workbook, sheet)
    worksheet = workbook.sheet_by_name(sheet)

    data = []
    for i in range(0, worksheet.nrows):
        data.append([worksheet.cell_value(i, j) for j in range(0, worksheet.ncols)])
    return data


if __name__ == '__main__':
    path = '/Users/luoxiangnan/PycharmProjects/flask-vue-demo/uploads/名单222.xlsx'
    print(read_sheet_names(path))
    print(read_sheet_merged_cells(path))
    data = read_excel_data(path)
    for i, row in enumerate(data):
        for j, v in enumerate(row):
            print('[{}, {}]'.format(i, j), v, "\t", end="")
        print()
