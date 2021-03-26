import torch

# 5 * 3 矩阵，不初始化
x = torch.empty(5, 3)
# print(x)

# 构造随机初始化矩阵
x = torch.rand(5, 3)
# print(x)

# 狗周矩阵全为0，数据为long
x = torch.zeros(5, 3, dtype=torch.long)
# print(x)

# 构造一个张量，直接使用数据
x = torch.tensor([5.5, 3])
# print(x)

x = x.new_ones(5, 3, dtype=torch.double)
# print(x)

x = torch.randn_like(x, dtype=torch.float)
# print(x)

# print(x.size())

# 加法1
y = torch.rand(5, 3)
# print(x + y)

# print(torch.add(x, y))

# 加法：提供一个输出tensor作为参数
result = torch.empty(5, 3)
torch.add(x, y, out=result)
# print(result)
# print(x)
# print(y)
# 加法：in-place
y.add_(x)
# print(y)

# print(x[:, 1])

x = torch.randn(4, 4)
y = x.view(16)
z = x.view(-1, 8)  # 从其他维推出
# print(x.size(), y.size(), z.size())

# 如果只有一个元素tensor .item()获得value
x = torch.randn(1)
# print(x)
# print(x.item())
