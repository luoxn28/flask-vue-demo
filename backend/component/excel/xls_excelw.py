import xlrd
import xlutils
import xlwt
from xlutils.copy import copy

from backend.component import copy_excel
from backend.component.excel.base import excelr

path = '/Users/luoxiangnan/PycharmProjects/flask-vue-demo/uploads/FvwmTq5pf1PeSxMQ0S6jI_zs9HjH.xls'
workbook = xlrd.open_workbook(path, formatting_info=True)
sheet = excelr.default_if_null(workbook, None)
print(sheet)

style_index = None
worksheet = workbook.sheet_by_name(sheet)
for i in range(0, worksheet.nrows):
    for j in range(0, worksheet.ncols):
        # print(worksheet.cell_value(i, j), '(' + str(worksheet.cell(i, j).ctype) + ')', end=", ")
        # print(worksheet.cell_value(i, j), worksheet.cell_xf_index(i, j),
        #       workbook.xf_list[worksheet.cell_xf_index(i, j)], end=", ")
        print(worksheet.cell_value(i, j), end=',')
        if i == 4 and j == 0:
            style_index = worksheet.cell_xf_index(i, j)
    print()

# 修改某个表格数据
# new_workbook = copy(workbook)
# new_worksheet = new_workbook.get_sheet(sheet)
# new_worksheet.write(3, 0, '啦啦啦22')
# new_workbook.save(path)

# 修改某个表格数据的字体颜色
# https://blog.csdn.net/haowells/article/details/37928175
# style = xlwt.easyxf('font: color red;')
# print(style_index, type(style_index))
new_workbook, style_list = copy_excel.copy(workbook)
new_worksheet = new_workbook.get_sheet(sheet)
# new_worksheet.write(4, 0, worksheet.cell_value(3, 0), style)
new_worksheet.write(0, 0, worksheet.cell_value(0, 0), style_list[style_index])
new_workbook.save(path)

# 修改某个表格数据的背景色
# style = xlwt.easyxf('pattern: pattern solid, fore_colour red;')
# new_workbook = copy(workbook)
# new_worksheet = new_workbook.get_sheet(sheet)
# new_worksheet.write(2, 0, worksheet.cell_value(2, 0), style)
# new_worksheet.write(3, 1, worksheet.cell_value(3, 0)+'1', xlwt.easyxf('font: color blue;'))
# new_workbook.save(path)

# 获取某列数据类型
# https://www.cnblogs.com/zhoujie/p/python18.html

# excel数据写入到sqlite
# https://blog.csdn.net/weixin_43894266/article/details/86821437
