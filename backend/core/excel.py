import logging
import os

from backend.component.excel import xls_excelr, xlsx_excelr
from backend.component.excel.base import excelr
from backend.core import excel_dict


# 读取数据库中数据，返回
def query_excel_data(filepath: str, sheet: str, lambda_code: str, head_value=1):
    if lambda_code:
        if 'int(v[0])' not in lambda_code:
            lambda_code = lambda_code.replace('v[0]', 'int(v[0])')
    logging.info('query_excel_data: {} {} {}'.format(os.path.basename(filepath), sheet, lambda_code))
    if not excel_dict.excel_filepath or filepath != excel_dict.excel_filepath:
        raise Exception('当前文件为 {}，请重新加载新文件 {}'
                        .format(os.path.basename(excel_dict.excel_filepath), os.path.basename(filepath)))

    result = []
    data = excel_dict.query_by_lambda(sheet, lambda_code, head_value)
    if data:
        # 设置列名 v[0] v[1] ...
        result.append([['v[{}]'.format(v), 0] for v in range(len(data[0]))])
    for i, row in enumerate(data):
        # 对前端展示index为string类型
        row[0] = str(row[0])
        result.append([[v, 0] for v in row])
    return result


# 执行对应的查询query_data表达式
def query_excel_data_by_query_data(filepath: str, sheet: str, query_data: list, head_value=1):
    if not excel_dict.excel_filepath or filepath != excel_dict.excel_filepath:
        raise Exception('当前文件为 {}，请重新加载新文件 {}'
                        .format(os.path.basename(excel_dict.excel_filepath), os.path.basename(filepath)))
    result = []
    data = excel_dict.query_by_query_data(sheet, query_data, head_value)
    if data:
        # 设置列名 v[0] v[1] ...
        result.append([['v[{}]'.format(v), 0] for v in range(len(data[0]))])
    for i, row in enumerate(data):
        # 对前端展示index为string类型
        row[0] = str(row[0])
        result.append([[v, 0] for v in row])
    return result


# 读取某个sheet所有内容
def read_excel_data(filepath, sheet=None):
    if excelr.excel_file_type(filepath) == excelr.XLSX:
        excel = xlsx_excelr
    else:
        excel = xls_excelr

    # 获取单元格列表（合并单元格首格=1，其他为-1，正常的单元格为0）
    # 结果格式为: [(左上角行, 右下角行, 左上角列, 右下角列)]
    merged_cells_map = {}
    merged_cells = excel.read_sheet_merged_cells(filepath, sheet)
    for v in merged_cells:
        for i in range(v[0], v[1]):
            for j in range(v[2], v[3]):
                merged_cells_map['{}:{}'.format(i, j)] = [-1]
        merged_cells_map['{}:{}'.format(v[0], v[2])] = [1, v[1] - v[0], v[3] - v[2]]

    result = []
    data, type = excel.read_excel_data(filepath, sheet)
    for i, row in enumerate(data):
        result_row = []
        for j, v in enumerate(row):
            cache = merged_cells_map.get('{}:{}'.format(i, j))
            if not cache:
                result_row.append([v, 0])
            else:
                vm = list(cache)
                vm.insert(0, v)
                result_row.append(vm)
        result.append(result_row)

    return result
