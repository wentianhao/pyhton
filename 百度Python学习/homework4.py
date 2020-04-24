import matplotlib.pyplot as plt
import numpy as np
import json
import matplotlib.font_manager as font_manager

with open('data/data31557/20200422.json','r',encoding='UTF-8') as file:
    json_array = json.loads(file.read())

# 绘制小姐姐区域分布柱状图，x轴为地区，y轴为该区域的小姐姐数量

zones = []

for star in json_array:
    zone = star['zone']
    zones.append(zone)
print(len(zones))
print(zones)

zone_list = []
count_list = []

for zone in zones:
    if zone not in zone_list:
        count = zones.count(zone)
        zone_list.append(zone)
        count_list.append(count)

print(zone_list)
print(count_list)

# 设置显示中文
plt.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体

plt.figure(figsize=(20,15))

plt.bar(range(len(count_list)),count_list,color='r',tick_label=zone_list,facecolor='#9999ff',edgecolor='white')

# 调节横坐标的倾斜度，rotation是度数，以及设置刻度字体大小
plt.xticks(rotation=45,fontsize=20)
plt.yticks(fontsize=20)

plt.legend()
plt.title('''《青春有你2》参赛选手''',fontsize = 24)
plt.savefig('work/result/bar_result.png')
plt.show()