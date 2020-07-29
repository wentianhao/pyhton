import numpy as np

def bag_0_1(weight, value, weight_most):  # return max value
    weight.insert(0, 0)  # 前0件要用
    value.insert(0, 0)  # 前0件要用
    bag = np.zeros((num + 1, weight_most + 1), dtype=np.float)  # 下标从零开始
    for i in range(1, num + 1):
        for j in range(1, weight_most + 1):
            if weight[i] <= j:
                bag[i][j] = max(bag[i - 1][int(round(j - weight[i]))] + value[i], bag[i - 1][j])
            else:
                bag[i][j] = bag[i - 1][j]
    # print(bag)
    return bag


def show(weight, result,weight_most):
    print('最大价值为:', result[num][weight_most])
    x=[0 for i in range(num)]
    j = weight_most
    for i in range(num,0,-1):
        if result[i][int(j)] > result[i-1][int(j)]:
            x[i-1] = 1
            j-=weight[i-1]
    print("背包中所装物品为：")
    for i in range(num):
        if x[i]:
            print("第",i+1,"个",end=' ')

if __name__ =='__main__':
    weight = [21.240115917020177, 18.411688792273985, 21.936741853424405, 21.080363026950906]
    print(weight[0]+weight[1])
    value = [10, 10, 10, 10]
    weight_most = 40
    num = len(weight)
    result = bag_0_1(weight, value, weight_most)
    show(weight,result,weight_most)