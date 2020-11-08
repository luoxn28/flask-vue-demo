"""
基于dict的excel内存数据库
"""
import logging
import os
import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp

from backend.component.excel import xlsx_excelr, xls_excelr
from backend.component.excel.base import excelr

logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)

# excel数据全局变量
ctype = {0: 'empty', 1: 'string', 2: 'number', 3: 'date', 4: 'boolean', 5: 'error'}
sheet_names = None
sheet_db = None
sheet_db_type = None

# excel当前信息
excel_filepath = None
excel_sheet = None


# 获取sheet列表
def read_sheet_names():
    return sheet_names if sheet_names else []


# 获取当前sheet信息
def current_sheet_name():
    filepath = excel_filepath if excel_filepath else ''
    sheet = excel_sheet if excel_sheet else (sheet_names[0] if sheet_names and len(sheet_names) == 1 else '')
    return [filepath, sheet]


# 加载excel文件到内存数据库
def load_excel_data(filepath: str):
    if excelr.excel_file_type(filepath) == excelr.XLSX:
        excel = xlsx_excelr
    else:
        excel = xls_excelr

    global excel_filepath
    excel_filepath = filepath
    logging.info('开始加载文件 ' + excel_filepath)

    # 读取sheet列表
    global sheet_names
    sheet_names = excel.read_sheet_names(filepath)

    # db结构：{sheet:[merged_cells:list, data_cells:dict]}
    global sheet_db, sheet_db_type
    sheet_db = {}
    sheet_db_type = {}
    for name in sheet_names:
        # 读取 [合并单元格列表, 表格数据]
        merged_cells = excel.read_sheet_merged_cells(filepath, name)
        sheet_db[name] = [merged_cells, {}]
        sheet_db_type[name] = {}
        data_cells, type_cells = excel.read_excel_data(filepath, name)

        df = pd.read_excel(filepath, name)
        df_data_cells = df.values
        for i, data in enumerate(data_cells):
            if i == 0:
                data.insert(0, i + 1)
                sheet_db[name][1][i + 1] = data
            else:
                df_row = list(df_data_cells[i - 1])
                df_row.insert(0, i + 1)
                sheet_db[name][1][i + 1] = [v if not pd.isna(v) else '' for v in df_row]
        for i, types in enumerate(type_cells):
            types.insert(0, 0)
            sheet_db_type[name][i + 1] = types

    logging.info('完成加载文件 {}, sheet_names:{}'.format(os.path.basename(filepath), sheet_names))
    return


# 执行对应的查询query_data表达式
def query_by_query_data(sheet: str, query_data: list, head_value=1):
    if not excel_filepath:
        raise Exception('未加载任何excel文件')
    if sheet not in sheet_db:
        raise Exception('sheet:{} 在文件{}中未找到'.format(sheet, os.path.basename(excel_filepath)))

    try:
        values = [v for v in sheet_db[sheet][1].values()]
        headers = values[0:head_value]
        values = values[head_value:]
        values.sort(key=lambda v: int(v[0]))
        for query in query_data:
            if ('input' not in query) or ('input_type' not in query):
                continue
            lambda_code = query['input']
            lambda_type = query['input_type']
            if not lambda_code:
                continue

            if lambda_type == 0:  # 表达式
                if 'int(v[0])' not in lambda_code:
                    lambda_code = lambda_code.replace('v[0]', 'int(v[0])')
                lambda_code = 'lambda v: {}'.format(lambda_code)
                logging.info("query_by_lambda {} {} ({})".format(sheet, lambda_code, type(lambda_code)))
                func = eval(lambda_code)
                values = [v for v in values if func(v)]
            elif lambda_type == 1 or lambda_type == 2:  # 排序 1:正序 2:倒序
                if 'v[0]' not in lambda_code:
                    lambda_code = lambda_code + ',v[0]'
                lambda_code = 'lambda v: ({})'.format(lambda_code)
                logging.info("query_by_sort {} {} ({})".format(sheet, lambda_code, type(lambda_code)))
                values = sorted(values, key=eval(lambda_code), reverse=False if lambda_type == 1 else True)

        result = headers + values
        for row in result:
            for i, item in enumerate(row):
                if isinstance(item, Timestamp):
                    row[i] = item.strftime("%Y-%m-%d %H:%M:%S")
        return result
    except Exception as e:
        print(e)
        raise e


if __name__ == '__main__':
    print(read_sheet_names())
    load_excel_data('/Users/luoxiangnan/PycharmProjects/flask-vue-demo/uploads/名单222.xlsx')
    print(read_sheet_names())
    print(current_sheet_name())
    print()

    print(sheet_db)
    print(sheet_db_type)

    # try:
    #     for v in query_by_query_data('Sheet0', [
    #         {'input': 'v[0]<10', 'input_type': 0},
    #         {'input': 'v[4]', 'input_type': 1}
    #     ]):
    #         print(v)
    # except Exception as e:
    #     print(e)

# try:
#     # lambda_code = """lambda v: 1 < v[0] < 10 and v[4] > 5 and v[5] < 20 and (v[4] + v[5] > 16)"""
#     lambda_codes = """v[0]<10 and v[4]>1"""
#     for v in query_by_lambda('Sheet0', lambda_code=lambda_codes):
#         print(v)
# except Exception as e:
#     print(str(e))

# namespace = {}
# code = """def hellocute(xx):
#         return  "name %s" %(xx)
#     """
# exec(code, namespace)
# print(namespace['hellocute']('aaa'))
#
# # lambda_code = """lambda x: str(x).zfill(5)"""
# # func = eval(lambda_code)
# # print(func('123'))
#
#
# func = eval(lambda_code)
#
# logging.info("creating log")
#
# for sheet in read_sheet_names():
#     db = sheet_db[sheet][1]
#     # data = [v for v in db.values() if 1 < v[0] < 10 and v[4] > 5 and v[5] < 20 and (v[4] + v[5] > 16)]
#     data = [v for v in db.values() if func(v)]
#     for v in data:
#         print(v)
#         # print([type(a) for a in v])
#         # print([ctype[v] for v in sheet_db_type[sheet][v[0]]])
