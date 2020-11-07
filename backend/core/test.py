from itertools import groupby
from operator import itemgetter
import openpyxl

from pandas import DataFrame

data = [
    [1, '张三', 12, '综合早教1'],
    [3, '李四', 13, '综合早教3'],
    [2, '张三', 19, '综合早教2']]
# data.sort(key=lambda v: (v[0]))

path = '/Users/luoxiangnan/PycharmProjects/flask-vue-demo/uploads/名单222.xlsx'
print(path[0:path.rindex('.')] + "-download")
print(path[path.rindex('.'):])

# func = eval("lambda v: (v[2])")
# data.sort(key=func)
# for v in data:
#     print(v)
# data = sorted(data, key=lambda v: (v[1], v[0]))
# for k, item in groupby(data, key=lambda v: v[1]):
#     print(k)
#     for i in item:
#         print(i)

# df = DataFrame(data)
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
