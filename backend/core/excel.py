import xlrd

from backend.component.base import excelr

from backend.component import xls_excelr, xlsx_excelr


# 读取某个sheet所有内容
def read_excel_data(filepath, sheet=None):
    type = excelr.excel_file_type(filepath)
    if type == excelr.XLSX:
        excel = xlsx_excelr
    else:
        excel = xls_excelr

    # 获取单元格列表（合并单元格首格=1，其他为-1，正常的单元格为0）
    merged_cells_map = {}
    merged_cells = excel.read_sheet_merged_cells(filepath, sheet)
    for v in merged_cells:
        for i in range(v[0], v[1]):
            for j in range(v[2], v[3]):
                merged_cells_map['{}:{}'.format(i, j)] = [-1]
        merged_cells_map['{}:{}'.format(v[0], v[2])] = [1, v[1] - v[0], v[3] - v[2]]

    result = []
    data = excel.read_excel_data(filepath, sheet)
    for i, row in enumerate(data):
        result_row = []
        for j, v in enumerate(row):
            cache = merged_cells_map.get('{}:{}'.format(i, j))
            if not cache:
                result_row.append([v, 0])
            else:
                cache.insert(0, v)
                result_row.append(cache)
        result.append(result_row)

    return result
