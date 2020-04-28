import xlrd,xlwt
import datetime
import random
# 打开需要操作的excel
excel = xlrd.open_workbook("./data.xlsx")

# 获取excel的sheet表
sheet = excel.sheet_by_name("Sheet1")
starttime = datetime.datetime(2016,8,1,0,00,00)
endtime = datetime.datetime(2016,8,1,0,30,0)

onetime = []
one = []
user = []
print("-------start----")
print("start", starttime)
print("end", endtime)

for i in range(1,sheet.nrows):
    row_i = sheet.row_values(i)
    d = xlrd.xldate_as_datetime(row_i[0],0)
    # print(i,": ",row_i)
    onetime = []
    if d > starttime and d <= endtime:
        onetime.append(row_i[2])
        onetime.append(row_i[4])
        onetime.append(row_i[7])
        onetime.append(row_i[9])
        onetime.append(random.uniform(0,200))
        onetime.append(-1)
        onetime.append(-1)
        one.append(onetime)
        # print("d",d)
        # print("onetime:",onetime)
    else:
        print("one:", one)
        print(len(one))
        user.append(one)
        # print("user:",user)
        one = []
        if d >= endtime:
            starttime = endtime
            print("start", starttime)
            endtime = endtime + datetime.timedelta(hours=0.5)
            print("end", endtime)
            onetime.append(row_i[2])
            onetime.append(row_i[4])
            onetime.append(row_i[7])
            onetime.append(row_i[9])
            onetime.append(random.uniform(0, 200))
            onetime.append(-1)
            onetime.append(-1)
            # print("onetime:", onetime)
            # print(len(onetime))
            one.append(onetime)

print("user:",user)
print(len(user))



