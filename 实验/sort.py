import xlrd
import xlwt
from xlutils.copy import copy

path = './data.xls'
x1 = xlrd.open_workbook(path)
x2 = copy(x1)

sheet1 = x1.sheet_by_name("sheet1")

rows = sheet1.nrows
cols = sheet1.ncols

# 统计所有的日期
data = set()
for i in range(rows):
    cell = sheet1.row_values(i)
    info = cell[2]
    infos = info.split(" ")
    time = infos[0]
    # print(user,summary,disease,doctor,time,status)
    data.add(time)

data = sorted(data)
print(len(data))
# # 新建sheet表a
# for name in data:
#     x2.add_sheet(name)
#     print(name)
#     x2.save(path)

for i in range(rows):
    cell = sheet1.row_values(i)
    # print(cell)
    user,summary,disease,doctor = cell[0],cell[1],cell[3],cell[4]
    info = cell[2]
    i = info.split('(')
    status = ''
    for x in i :
        if ')' in x:
            status = x.rstrip().strip(')')


    infos = info.split(" ")
    time = infos[0]
    # print(user,summary,disease,doctor,time,status)


    if time in x1.sheet_names():
        table = x2.get_sheet(time)
        k = len(table.rows)
        # print(cell)
        # print(cell[0],cell[1],cell[2],cell[3],cell[4])
        table.write(k, 0, user)
        table.write(k,1,summary)
        table.write(k,2,time)
        table.write(k,3,status)
        table.write(k,4,disease)
        table.write(k,5,doctor)

        x2.save(path)
        print(time)



