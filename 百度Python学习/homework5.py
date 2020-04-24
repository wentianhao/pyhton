import matplotlib.pyplot as plt
import numpy as np
import json
import matplotlib.font_manager as font_manager
import pandas as pd

#显示matplotlib生成的图形
# %matplotlib inline


df = pd.read_json('data/data31557/20200422.json')
print(df)

grouped=df['name'].groupby(df['zone'])
s = grouped.count()

zone_list = s.index
count_list = s.values


# 设置显示中文
plt.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体

plt.figure(figsize=(20,15))

plt.bar(range(len(count_list)), count_list,color='r',tick_label=zone_list,facecolor='#9999ff',edgecolor='white')

# 这里是调节横坐标的倾斜度，rotation是度数，以及设置刻度字体大小
plt.xticks(rotation=45,fontsize=20)
plt.yticks(fontsize=20)

plt.legend()
plt.title('''《青春有你2》参赛选手''',fontsize = 24)
plt.savefig('work/result/bar_result02.png')
plt.show()