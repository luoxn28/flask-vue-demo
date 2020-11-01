import xlrd
from xlutils.filter import process, XLRDReader, XLWTWriter


# 复制一个excel文件，原生的xlutils.copy未返回style_list
# https://www.pythonf.cn/read/71719
def copy(wb: xlrd.book.Book):
    w = XLWTWriter()
    process(XLRDReader(wb, 'unknown.xls'), w)
    return w.output[0][1], w.style_list
