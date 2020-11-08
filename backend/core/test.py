from itertools import groupby
from operator import itemgetter
import openpyxl

from pandas import DataFrame
import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp

data = [
    [1, '张三', 12, '综合早教1'],
    [3, '李四', 13, '综合早教3'],
    [2, '张三', 19, '综合早教2']]
# data.sort(key=lambda v: (v[0]))

df = DataFrame(data)
print(df.iloc[:, 1:])

# path = '/Users/luoxiangnan/PycharmProjects/flask-vue-demo/uploads/名单222 (1).xlsx'
# path = '/Users/luoxiangnan/PycharmProjects/flask-vue-demo/uploads/名单222.xlsx'
# df = pd.read_excel(path, header=0)
# for row in df.values:
#     for item in row:
#         if isinstance(item, Timestamp):
#             print(item.strftime("%Y-%m-%d %H:%M:%S"), end=' ')
#         else:
#             print(item, end=' ')
#     print()

# df.to_excel('zzz.xlsx', sheet_name='Sheet1', index=False)

# func = eval("lambda v: (v[2])")
# data.sort(key=func)
# for v in data:
#     print(v)
# data = sorted(data, key=lambda v: (v[1], v[0]))
# for k, item in groupby(data, key=lambda v: v[1]):
#     print(k)
#     for i in item:
#         print(i)


# df = df.sort_values(0)
# df.apply(lambda x:x['v'])

# print(df)
# print(df.groupby(1, axis=1).groups)

# 按照列维度过滤，相当于保留一部分列
# df = df.filter(items=[0, 1], axis=1)
# 保存到excel
# df.to_excel('zzz.xlsx', sheet_name='Sheet1', index=False, header=False)

# if data:
#     print([['v[{}]'.format(v), 0] for v in range(len(data[0]))])
