from scipy.optimize import minimize
import numpy as np

# 计算 1/x + x 的最小值
def fun(x):
    return 1/x[0] + x[0]

x0 = np.asarray((1))
res = minimize(fun,x0,method="SLSQP")
x = res.x

print("x:",x[0])
print(fun(x))

# 计算 (2+x1)/(1+x2)-3*x1+4*x3的最小值，x1,x2,x3∈(0.1,0.9)
def fun2(x):
    return (2+x[0])/(1+x[1])-3*x[0]+4*x[2]

# ineq : 表示大于等于0
# eq : 表示等于0

# x-0.1 >= 0
def constraint1(x):
    return x[0]-0.1

# 0.9-x > =0
def constraint2(x):
    return -(x[0]-0.9)

def constraint3(x):
    return x[1]-0.1
def constraint4(x):
    return -(x[1]-0.9)
def constraint5(x):
    return x[2]-0.1
def constraint6(x):
    return -(x[2]-0.9)

con1 = {'type':'ineq','fun':constraint1}
con2 = {'type':'ineq','fun':constraint2}
con3 = {'type':'ineq','fun':constraint3}
con4 = {'type':'ineq','fun':constraint4}
con5 = {'type':'ineq','fun':constraint5}
con6 = {'type':'ineq','fun':constraint6}
cons = ([con1,con2,con3,con4,con5,con6])

x0 = np.array([0,0,0])

res = minimize(fun2,x0,method="SLSQP",constraints=cons)
x = res.x
print("x1:",x[0])
print("x2:",x[1])
print("x3:",x[2])
print(fun2(x))

# 目标函数
def objective(x):
	return x[0] ** 2 + x[1] ** 2 + x[2] ** 2 + 8


# 约束条件
def constraint1(x):
	return x[0] ** 2 - x[1] + x[2] ** 2  # 不等约束


def constraint2(x):
	return -(x[0] + x[1] ** 2 + x[2] ** 2 - 20)  # 不等约束


def constraint3(x):
	return -x[0] - x[1] ** 2 + 2


def constraint4(x):
	return x[1] + 2 * x[2] ** 2 - 3  # 不等约束


# 边界约束
# b = (0.0, None)
# bnds = (b, b, b)

con1 = {'type': 'ineq', 'fun': constraint1}
con2 = {'type': 'ineq', 'fun': constraint2}
con3 = {'type': 'eq', 'fun': constraint3}
con4 = {'type': 'eq', 'fun': constraint4}
cons = ([con1, con2, con3, con4])  # 4个约束条件
x0 = np.array([0, 0, 0])
# 计算
solution = minimize(objective, x0, method='SLSQP',constraints=cons)
x = solution.x

print('目标值: ' + str(objective(x)))
print('答案为')
print('x1 = ' + str(x[0]))
print('x2 = ' + str(x[1]))

# ----------------------------------
# 输出：
# 目标值: 10.651091840572583
# 答案为
# x1 = 0.5521673412903173
# x2 = 1.203259181851855
