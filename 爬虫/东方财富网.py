import requests
from bs4 import BeautifulSoup
import time
import csv
import re

# 复制请求头
head = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'max-age=0',
'Connection':'keep-alive',
'Cookie':'__guid=76223875.1610812464114072800.1562940006020.6155; em_hq_fls=js; intellpositionL=1076.26px; intellpositionT=2688.33px; HAList=a-sz-300002-%u795E%u5DDE%u6CF0%u5CB3%2Ca-sz-300001-%u7279%u9510%u5FB7%2Ca-sz-000009-%u4E2D%u56FD%u5B9D%u5B89%2Ca-sz-000010-*ST%u7F8E%u4E3D%2Ca-sh-600698-*ST%u5929%u96C1%2Ca-sh-601360-%u4E09%u516D%u96F6%2Ca-sz-300459-%u91D1%u79D1%u6587%u5316%2Ca-sh-600617-%u56FD%u65B0%u80FD%u6E90%2Ca-sz-300059-%u4E1C%u65B9%u8D22%u5BCC; qgqp_b_id=9a0c354a2a94284d66082f97f4e79ee7; ct=QFJ-8LWC_B2M_QvK4Jd7mWfAdDm2t18K50UdiCDU-u_QKnFgyBrF16g1nkXwS5Vr4c9XJ87DtuxKOB40AumJeyeHngZ0othkpa8q2FwHc3rVXFfsuXH7YCFlOQ326PYVzM7Za01btJuc7ISNPpzfAT7wOTgJroPrsBcch0nDGl8; ut=FobyicMgeV52Ad4fCxim_O1dpAWbFoUUHQnsTXfHjDCF4fVmXUX2Tgx0mCdY4JFogbJTxfbvFvHZ4KC-oHDlf9rs1W703aHK2sdioMbBAZjjiQrp0eOCY76KDSJRWlabyF0FCzSd35CFRvn5lofjembf0QQI-v3RyGoCyv-iZE23gE2zG2Ni8Hg0h6OkTHR1hesTf0gv-FMPhAkyCs52Ol-IqApU1KdR2VcP25Ol-RnlOHkED1cGEwEp9_2l7p5Vs043omSwlv1hUor8MXxMDnNjlqPxvSsU; pi=5005305879999664%3by5005305879999664%3b%e8%82%a1%e5%8f%8b0UQUzz%3bD6hQBIYBMbA4JFeWmeryVdOOhKxncZp0aIhgTi3HPGfbUMzn7zExs8O%2fCUgA8XyPy1%2b0drNcd5vfA9twAbKxNAhKbuOvVBUUp0j%2bXEI9oPhTVhrRRDqMdGJk5npR9ntJn90kDK5x4ZgkBUhDr8H%2b8LbzD%2b4U3vTQFs%2fufMEkO3ndToTchsT9OP5qrfkqhXai3lEDbp9E%3bD0o0KllCqBVrHpHxuIaeDzjZPbG6i5UeQpLjSyPaA%2f26zBQLHPDDFXHfmDZNDQFs40KIZAzV4mKwjAbeNy6Y2Eo3QNGcwBd3q6QkCBEcR5w3pVdVj6Nahea1c73%2bNaGGfreYvR0g1W4jiDW%2fdZuy%2fxq8j6T1Pw%3d%3d; uidal=5005305879999664%e8%82%a1%e5%8f%8b0UQUzz; st_si=07099573969353; _adsame_fullscreen_18009=1; emshistory=%5B%22%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%22%2C%22%E8%82%A1%E7%A5%A8%E5%B8%82%E5%9C%BA%22%2C%22%E5%90%91%E6%97%A5%E8%91%B5%22%2C%22111%22%5D; st_pvi=32364422128612; st_sp=2019-07-12%2022%3A00%3A08; st_inirUrl=http%3A%2F%2Fwww.so.com%2Flink; st_sn=39; st_psi=20200428161400835-117001301474-7621177606; st_asi=delete; monitor_count=80',
'Host': 'guba.eastmoney.com',
'Referer':'http://guba.eastmoney.com/',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

# 设置数据存储方式，csv表格写入
f = open('szzs.csv', 'a', newline='')
w = csv.writer(f)


# 获取帖子详细时间，列表也没有年份，可以作为获取帖子其他详细内容的通用方法
def get_time(url):
    try:
        q = requests.get(url, headers=head)
        soup = BeautifulSoup(q.text, 'html.parser')

        ptime = soup.find('div', {'class': 'zwfbtime'}).get_text()
        ptime = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', ptime)[0]
        ptitle = soup.find('div',{'id':'zwconttbt'}).get_text()

        return ptitle,ptime
    except:
        return ''


# 获取列表页第n页的具体目标信息，由BeautifulSoup解析完成
def get_urls(url):
    baseurl = 'http://guba.eastmoney.com/'
    q = requests.get(url, headers=head)
    soup = BeautifulSoup(q.text, 'html.parser')
    urllist = soup.findAll('div', {'class': 'articleh'})
    print(len(urllist))
    time.sleep(1)
    for i in urllist:
        if i.find('a') != None:
            try:
                detailurl = i.find('a').attrs['href'].replace('/', '')
                print(detailurl)
                # titel = i.find('a').get_text()
                yuedu = i.find('span', {'class': 'l1'}).get_text()
                pinlun = i.find('span', {'class': 'l2'}).get_text()
                titel,ptime = get_time(baseurl + detailurl)
                # ptime = i.find('span',{'class':'l5'}).get_text()
                print(titel,yuedu,pinlun,ptime)
                w.writerow([detailurl, titel, yuedu, pinlun, ptime])
                # print(baseurl + detailurl)
            except:
                pass


# 循环所有页数
for i in range(1,2):
    # print(i)
    get_urls('http://guba.eastmoney.com/list,zssh000001,f_' + str(i) + '.html')

