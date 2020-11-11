import torch as t

batch_size = 2
time_steps = 10
features = 2
# 返回一个包含未初始化数据的张量。
data = t.empty(batch_size, time_steps, features).normal_()
# print(data.shape)  #  torch.Size([2, 10, 2])

lstm = t.nn.LSTM(input_size=2, hidden_size=3, num_layers=2,bidirectional=True, batch_first=True)

output, (h_n, c_n) = lstm(data)

print(output.shape,h_n.shape,c_n.shape)
# torch.Size([2, 10, 6]) torch.Size([2, 2, 3]) torch.Size([2, 2, 3])

class Net(t.nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm1 = t.nn.LSTM(input_size=2,hidden_size=3,bidirectional=True,batch_first=True)
        self.lstm2 = t.nn.LSTM(input_size=2*3,hidden_size=3,bidirectional=True,batch_first=True)

    def forward(self,input):
        output,(h_n,c_n) = self.lstm1(input)
        output,(h_n,c_n) = self.lstm2(output)
        return output

net = Net()
print(net(data).shape)
# torch.Size([2, 10, 8])
