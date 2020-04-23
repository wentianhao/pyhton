# 导入OS模块
import os
# 待搜索的目录路径
path = "Day1-homework"
# 待搜索的名称
filename = "2020"
# 定义保存结果的数组
result = []

def findfiles():
    # 查找文件
    fileList = os.walk(path)

    for root,dirs,files in fileList:
        for file in files:
            if filename in file:
                name = os.path.join(root,file)
                result.append(name)

    for i in result:
        print(result.index(i)+1,i)

if __name__ == '__main__':
    findfiles()