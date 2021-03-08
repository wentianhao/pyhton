from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import GeoType
import xlrd,xlwt

def geo(path):
    city = '上海'
    g = Geo()
    g.add_schema(maptype=city)

    # 定义坐标对应的名称，添加到坐标库中 add_coordinate(name, lng, lat)
    # g.add_coordinate('1', 121.422, 31.274)
    # g.add_coordinate('2', 121.401, 31.281)
    # g.add_coordinate('3', 121.509, 31.272)

    # 定义数据对，
    # data_pair = [('1', 10), ('2', 5), ('3', 20),('2',30)]
    data_pair = []
    # print(type(data_pair[0]))

    data = getData(path)
    for d in data:
        g.add_coordinate(str(d[0]),d[1],d[2])
        data_pair.append(tuple((str(d[0]),5)))


    # Geo 图类型，有 scatter, effectScatter, heatmap, lines 4 种，建议使用
    # from pyecharts.globals import GeoType
    # GeoType.GeoType.EFFECT_SCATTER，GeoType.HEATMAP，GeoType.LINES

    # 将数据添加到地图上
    g.add('', data_pair, type_=GeoType.EFFECT_SCATTER, symbol_size=2)
    # 设置样式
    g.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    # 自定义分段 color 可以用取色器取色
    pieces = [
        {'max': 1, 'label': '0以下', 'color': '#50A3BA'},
        {'min': 1, 'max': 10, 'label': '1-10', 'color': '#3700A4'},
        {'min': 10, 'max': 20, 'label': '10-20', 'color': '#81AE9F'},
        {'min': 20, 'max': 30, 'label': '20-30', 'color': '#E2C568'},
        {'min': 30, 'max': 50, 'label': '30-50', 'color': '#FCF84D'},
        {'min': 50, 'max': 100, 'label': '50-100', 'color': '#DD0200'},
        {'min': 100, 'max': 200, 'label': '100-200', 'color': '#DD675E'},
        {'min': 200, 'label': '200以上', 'color': '#D94E5D'}  # 有下限无上限
    ]
    #  is_piecewise 是否自定义分段， 变为true 才能生效
    g.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pieces),
        title_opts=opts.TitleOpts(title="{}-店铺分布".format(city)),
    )
    return g

def getData(path):
    excel = xlrd.open_workbook(path)
    sheet = excel.sheet_by_name('Sheet1')
    data = []
    rows = sheet.nrows
    for i in range(1,rows):
        row_i = sheet.row_values(i)
        row_i[0] = xlrd.xldate_as_datetime(row_i[0], 0)
        data.append(row_i)
    return data

p = 'd1'
path = 'data/'+p+'.xlsx'

g = geo(path)
# 渲染成html, 可用浏览器直接打开
g.render('test_render_'+p+'.html')
