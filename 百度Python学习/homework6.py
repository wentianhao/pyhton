import matplotlib.pyplot as plt
import numpy as np
import json
import matplotlib.font_manager as font_manager
import pandas as pd

#显示matplotlib生成的图形
# %matplotlib inline


df = pd.read_json('data/data31557/20200422.json')
# print(df)

grouped=df['name'].groupby(df['weight'])
s = grouped.count()

weight_list = s.index
count_list = s.values

d = {'<45kg':0,'45~50kg':0,'50~55kg':0,'>55kg':0}

for weight in weight_list:
    if weight < '45kg':
        d['<45kg'] = d['<45kg'] + s[weight]
    elif weight < '50kg':
        d['45~50kg'] = d['45~50kg'] + s[weight]
    elif weight < '55kg':
        d['50~55kg'] = d['50~55kg'] + s[weight]
    else:
        d['>55kg'] = d['>55kg'] + s[weight]

color = ['blue','orange','green','red'] # 各部分颜色
explode = [0,0.05,0,0]

"""
绘制饼图
explode：设置各部分突出
label:设置各部分标签
labeldistance:设置标签文本距圆心位置，1.1表示1.1倍半径
autopct：设置圆里面文本
shadow：设置是否有阴影
startangle：起始角度，默认从0开始逆时针转
pctdistance：设置圆内文本距圆心距离
返回值
l_text：圆内部文本，matplotlib.text.Text object
p_text：圆外部文本
"""

patches, l_text, p_text = plt.pie(d.values(), explode=explode, colors=color, labels=d.keys(), labeldistance=1.1, autopct="%1.1f%%", shadow=False, startangle=90, pctdistance=0.6)
plt.axis("equal")    # 设置横轴和纵轴大小相等，这样饼才是圆的
plt.legend()
plt.savefig('work/result/pie_result.png')
plt.show()

