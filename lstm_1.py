# https://www.cnblogs.com/tecdat/p/11757372.html
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

data_csv=pd.read_excel('./regionminute10_15.xlsx',usecols=[13],header=None)
# 数据预处理
data_csv = data_csv.dropna()  # 滤除缺失数据
dataset = data_csv.values   # 获得csv的值

'''
任务根据前108天来预测最近12天内骑行人数。
有120天的记录，前108天的数据将用于训练我们的LSTM模型，
而模型性能将使用最近12天的值进行评估。
'''
# 绘制每天骑行人数的频率
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 15
fig_size[1] = 5
plt.rcParams["figure.figsize"] = fig_size
plt.title('Ten mins vs Rider')
plt.ylabel('Total Rider')
plt.xlabel('Minutes')
plt.grid(True)
plt.autoscale(axis='x',tight=True)
plt.plot(dataset)
plt.savefig('MinvsRider.png')
plt.show()

# 将数据的类型改为float
all_data = dataset.astype('float32')
print(all_data)

test_data_size = 12
#
train_data = all_data[:-test_data_size]
# print("t",train_data)
test_data = all_data[-test_data_size:]
# print("test",test_data)

'''
数据集规范化，标准化数据以进行时间序列预测非常重要
在一定范围内的最小值和最大值之间对数据进行规范化。
使用模块中的MinMaxScaler类sklearn.preprocessing来扩展数据
分别将最大值和最小值分别为-1和1归一化
数据标准化仅应用于训练数据，而不应用于测试数据。
如果对测试数据进行归一化处理，
则某些信息可能会从训练集中 到测试集中。
'''
scaler = MinMaxScaler(feature_range=(-1,1))
train_data_normalized = scaler.fit_transform(train_data.reshape(-1,1))
# print(train_data_normalized[:5])
# print(train_data_normalized[-5:])
# print("归一化：",train_data_normalized)
'''
将数据集转换为张量，
因为PyTorch模型是使用张量训练的。
要将数据集转换为张量
将数据集传递给FloatTensor对象的构造函数
'''
train_data_normalized = torch.FloatTensor(train_data_normalized).view(-1)
#
# # print("张量:",train_data_normalized)
#
'''
最后的预处理步骤是将训练数据转换为序列和相应的标签。s
可以使用任何序列长度，这取决于领域知识
在我们的数据集中，使用12的序列长度很方便，
因为我们有月度数据，一年中有12个月。
如果我们有每日数据，则更好的序列长度应该是365，即一年中的天数。
因此，我们将训练的输入序列长度设置为12。
'''
train_window = 12

'''
将定义一个名为的函数create_inout_sequences。
该函数将接受原始输入数据，并将返回一个元组列表。
在每个元组中，第一个元素将包含与12天内旅行的乘客数量相对应的12个项目的列表，
第二个元组元素将包含一个项目，即在12 + 1天内的乘客数量。
'''
def create_inout_sequences(input_data,tw):
    inout_seq = []
    L = len(input_data)
    for i in range(L-tw):
        # print("i:",i)
        train_seq = input_data[i:i+tw]
        train_label = input_data[i+tw:i+tw+1]
        inout_seq.append((train_seq,train_label))
        # print((train_seq,train_label))
    return inout_seq

train_inou_seq = create_inout_sequences(train_data_normalized,train_window)

'''
创建LSTM模型，LSTM该类的构造函数接受三个参数：
input_size：对应于输入中的要素数量。
尽管我们的序列长度为12，但每个月我们只有1个值，即乘客总数，因此输入大小为1。
hidden_layer_size：指定隐藏层的数量以及每层中神经元的数量。我们将有一层100个神经元。
output_size：输出中的项目数，由于我们要预测未来1个月的乘客人数，因此输出大小为1。
在构造函数中，我们创建变量hidden_layer_size，lstm，linear，和hidden_cell。
LSTM算法接受三个输入：先前的隐藏状态，先前的单元状态和当前输入。
该hidden_cell变量包含先前的隐藏状态和单元状态的lstm和linear层变量用于创建LSTM和线性层。

在forward方法内部，将input_seq作为参数传递，该参数首先传递给lstm图层。
lstm层的输出是当前时间步的隐藏状态和单元状态，以及输出。
lstm图层的输出将传递到该linear图层。
预计的乘客人数存储在predictions列表的最后一项中，并返回到调用函数。

下一步是创建LSTM()类的对象，定义损失函数和优化器。由于我们正在解决分类问题，
'''
class LSTM(nn.Module):
    def __init__(self,input_size=1,hidden_layer_size=100,output_size=1):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size

        self.lstm = nn.LSTM(input_size=input_size,hidden_size=hidden_layer_size,num_layers=2)

        self.linear = nn.Linear(hidden_layer_size,output_size)

        self.hidden_cell = (torch.zeros(1,1,self.hidden_layer_size),
                            torch.zeros(1,1,self.hidden_layer_size))

    def forward(self,input_seq):
        lstm_out,self.hidden_cell = self.lstm(input_seq.view(len(input_seq),1,-1),self.hidden_cell)
        predictions = self.linear(lstm_out.view(len(input_seq),-1))
        return predictions[-1]

model = LSTM()
loss_function = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(),lr=0.001)
# print(model)

epochs = 1000
for i in range(epochs):
    for seq,labels in train_inou_seq:
        optimizer.zero_grad()
        model.hidden_cell = (torch.zeros(1,1,model.hidden_layer_size),
                             torch.zeros(1,1,model.hidden_layer_size))
        y_pred = model(seq)

        single_loss = loss_function(y_pred,labels)
        single_loss.backward()
        optimizer.step()

    if i%25 ==1:
        print(f'epoch: {i:3} loss: {single_loss.item():10.8f}')

print(f'epoch:{i:3} loss:{single_loss.item():10.10f}')

fut_pred = 12
test_inputs = train_data_normalized[-train_window:].tolist()
# print(test_inputs)

model.eval()

for i in range(fut_pred):
    seq = torch.FloatTensor(test_inputs[-train_window:])
    with torch.no_grad():
        model.hidden = (torch.zeros(1,1,model.hidden_layer_size),
                        torch.zeros(1,1,model.hidden_layer_size))
        test_inputs.append(model(seq).item())

test = test_inputs[fut_pred:]
# print(test)

predictions = scaler.inverse_transform(np.array(test_inputs[train_window:]).reshape(-1,1))
print(predictions)
actual_predictions = []
# 人数取整，四舍五入
for d in predictions:
    p = []
    p.append(round(d[0]))
    actual_predictions.append(p)
print(actual_predictions)
x = np.arange(108,120,1)
# print(x)

plt.title('Mins vs Rider')
plt.ylabel('Total Riders')
plt.grid(True)
plt.autoscale(axis='x', tight=True)
plt.plot(dataset)
plt.plot(x,actual_predictions)
plt.savefig('MinvsRider1.png')
plt.show()


plt.title('Mins vs Rider')
plt.ylabel('Total Riders')
plt.grid(True)
plt.autoscale(axis='x', tight=True)
plt.plot(x,dataset[-train_window:])
plt.plot(x,actual_predictions)
plt.savefig('MinvsRider2.png')
plt.show()
