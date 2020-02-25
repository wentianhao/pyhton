import xlrd
import xlwt
from xlutils.copy import copy

path = './data1.xls'
x1 = xlrd.open_workbook(path)
x2 = copy(x1)

sheet1 = x1.sheet_by_name("sheet1")

rows = sheet1.nrows
cols = sheet1.ncols

# 统计所有的
days = set()
# print(range(rows))
for i in range(rows):
    cell = sheet1.row_values(i)
    info = cell[2]
    infos = info.split(" ")
    time = infos[0]
    inf = info.split('(')
    s = ''
    day = 0
    for x in inf :
        if ')' in x:
            s = x.rstrip().strip(')')
            # print(s)
            if '当天' in s:
                day = 0
                # print(day)
            else:
                s = s.lstrip().strip('就诊后')
                day = s.rstrip().strip('天')
                # print(day)
                if 'xx' not in day:
                    day = int(day)
                # print(day)
            days.add(day)
print(days)
#
# 新建sheet表
for name in days:
    if name == 0:
        n = "就诊当天"
    else:
        n = "就诊后"+str(name)+"天"
    x2.add_sheet(n)
    print(n)
    x2.save(path)
#
#
# print(x1.sheet_names())
q = 0
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
#             # print(status)
#
#
    infos = info.split(" ")
    time = infos[0]
    # print(user,summary,disease,doctor,time,status)
#

    if status in x1.sheet_names():
        q=q+1
        # print(q)
        table = x2.get_sheet(status)
        k = len(table.rows)
        # print(cell,table)
        # print(cell[0],cell[1],cell[2],cell[3],cell[4])
        table.write(k, 0, user)
        table.write(k,1,summary)
        table.write(k,2,time)
        table.write(k,3,status)
        table.write(k,4,disease)
        table.write(k,5,doctor)
        print(status)
        print(q)
        x2.save(path)
    else:
        q=q+1
        # print(status)
        status="就诊当天"
        table = x2.get_sheet(status)
        k = len(table.rows)
        # print(cell,table)
        # print(cell[0],cell[1],cell[2],cell[3],cell[4])
        table.write(k, 0, user)
        table.write(k,1,summary)
        table.write(k,2,time)
        table.write(k,3,status)
        table.write(k,4,disease)
        table.write(k,5,doctor)
        print(status)
        print(q)
        x2.save(path)
    #     print(time,x1.sheet_names())
#
#
#
print(cols)
print(rows)