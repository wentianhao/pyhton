# pytorch 自动微分
# 如果将属性 .requires_grad 设置为 true ,则会开始跟踪针对tensor的所有操作
# 完成计算后，可以调用 .backward() 来自动计算所有梯度，该张量的梯度将累积导 .grad 属性中
# 停止 tensor历史记录的跟踪 ， 调用 .detach() ,它将其与计算历史记录分离，并防止将来的计算被跟踪
# 停止跟踪历史记录（和使用内存）， 使用 with torch.no_grad() 包装起来。
# 在评估模型时，这是特别有用，因为模型在训练阶段具有 requires_grad = True 的可训练参数有利于调参，但在评估阶段我们不需要梯度。
# Tensor 和 Function 互相连接并构建一个非循环图，它保存整个完整的计算过程的历史信息。
# 每个张量都有一个 .grad_fn 属性保存着创建了张量的 Function 的引用，（如果用户自己创建张量，则grad_fn 是 None ）。
# 计算导数 调用 Tensor.backward()。
# 如果 Tensor 是标量（即它包含一个元素数据），则不需要指定任何参数backward()，
# 但是如果它有更多元素，则需要指定一个gradient 参数来指定张量的形状
import torch

# 跟踪相关计算
x = torch.ones(2, 2, requires_grad=True)
# print(x)
y = x + 2
# print(y)
# print(y.grad_fn)
z = y * y * 3
out = z.mean()
# print(z, out)

a = torch.randn(2, 2)
a = (a * 3) / (a - 1)
# print(a.requires_grad)
a.requires_grad_(True)
# print(a.requires_grad)
b = (a * a).sum()
# print(b.grad_fn)
# print(b.requires_grad)

# 梯度
out.backward()
# print(x.grad)

# 雅可比向量机
x = torch.randn(3, requires_grad=True)
y = x * 2
# print(y)
# print(y.data)
# print(y.data.norm())
while y.data.norm() < 1000:
    y = y * 2

# print(y)

v = torch.tensor([0.1, 1.0, 0.0001], dtype=torch.float)
y.backward(v)
print(x.grad)

print(x.requires_grad)
print((x ** 2).requires_grad)
# 将代码包裹在 with torch.no_grad()，来停止对从跟踪历史中 的 .requires_grad=True 的 张量自动求导
with torch.no_grad():
    print((x ** 2).requires_grad)
