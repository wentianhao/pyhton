# 一个典型的神经网络训练过程包括以下几点：
# 1.定义一个包含可训练参数的神经网络
# 2.迭代整个输入
# 3.通过神经网络处理输入
# 4.计算损失(loss)
# 5.反向传播梯度到神经网络的参数
# 6.更新网络的参数，典型的简单更新方法: weight = weight - learning_rate * geadient

# 定义神经网络
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        # 1 input image channel , 6 output channels, 5 * 5 square convolution
        # kernel
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        # an affine operation: y =Wx + b
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # Max pooling over a (2,2) window
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # if the size is a square you can only specify a single number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features


net = Net()
# print(net)

# 2. 一个模型可训练的参数可以通过调用 net.parameters()返回
params = list(net.parameters())
# print(len(params))
# print(params[0].size())

# 32*32 输入
input_data = torch.randn(1, 1, 32, 32)
# print(input_data)
out = net(input_data)
# print(out)

# 把所有参数梯度缓存器置0，用随机的梯度来反向传播
net.zero_grad()
out.backward(torch.randn(1, 10))

# 3. 损失函数
# 一个损失函数需要一对输入：模型输出和目标，然后计算一个值来评估输出距离目标有多远
# nn.MSELoss 计算均方误差
output = net(input_data)
print(output)
target = torch.rand(10)
print(target)
target = target.view(1, -1)
print(target)
criterion = nn.MSELoss()

loss = criterion(output, target)
print(loss)

# input_data  --> conv2d --> relu --> maxpool2d --> conv2d --> relu --> maxpool2d
#             --> view --> linear --> relu --> linear --> relu --> linear
#             --> MSELoss
#             --> loss

print(loss.grad_fn)  # MSELoss
print(loss.grad_fn.next_functions[0][0])  # linear
print(loss.grad_fn.next_functions[0][0].next_functions[0][0])  # ReLU

# 反向传播
net.zero_grad()

print('conv1.bias.grad before backward')
print(net.conv1.bias.grad)

loss.backward()

print('conv1.bias.grad after backward')
print(net.conv1.bias.grad)

# 更新神经网络参数
# 最简单的 更新规则 ： 随机梯度下降
# weight = weight - learnin_rate * gradient
learning_rate = 0.01
for f in net.parameters():
    f.data.sub_(f.grad.data * learning_rate)

# 想使用不同的更新规则，类似于SGD,Nesterov-SGD,Adam,RMSProp等 ，torch.optim实现了所有方法

# create your optimizer
optimizer = optim.SGD(net.parameters(), lr=0.01)

# in your training loop:
optimizer.zero_grad()
output = net(input_data)
loss = criterion(output, target)
loss.backward()
optimizer.step() # does the update
