import urllib.request
import re
import random
import http.cookiejar

keyname = "Python"
key = urllib.request.quote(keyname)
uapools=[
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363"
]

# cookiename = './cookie.txt'
# # 声明一个CookieJar对象实例来保存cookie
# cookie = http.cookiejar.MozillaCookieJar(filename=cookiename)
# # 利用urllib库中的request的HTTPCookieProcessor对象来创建cookie处理器
# handler = urllib.request.HTTPCookieProcessor(cookie)
# # 通过handle来构建opener
# opener = urllib.request.build_opener(handler)
# # 此处的open方法同urllib的urlopen方法一样
# response = opener.open("https://www.taobao.com/")
# # 保存cookie 文件
# cookie.save(ignore_discard=True,ignore_expires=True)

def ua(uapools):
    thisua = random.choice(uapools)
    print(thisua)
    headers = ("User-Agent",thisua)
    opener = urllib.request.build_opener()
    opener.addheaders=[headers]
    # 安装为全局
    urllib.request.install_opener(opener)

#一共 101 页
for i in range(1,101):
    print("-----------第"+str(i)+"页商品----------")
    url = "https://s.taobao.com/search?q="+key+"&s="+str((i-1)*44)
    print(url)
    ua(uapools)
    data = urllib.request.urlopen(url).read().decode("utf-8","ignore")
    print(data)
    pat = '"nid":"(.*?)"'
    idlist = re.compile(pat,re.S).findall(data)
    for j in range(0,len(idlist)):
        thisid = idlist[j]
        thisurl = "https://detail.tmall.com/item.htm?id="+str(thisid)
        itemdata = urllib.request.urlopen(thisurl).read().decode("gbk","ignore")
        titlepat = '"raw_title":"(.*?)"'
        detailpat = '"detail_url":"(.*?)"'
        pricepat = '"view_price":"(.*?)"'
        title = re.compile(titlepat,re.S).findall(itemdata)
        if(len(title) > 0):
            title = title[0]
        else:
            continue
        detail = re.compile(detailpat,re.S).findall(itemdata)
        if (len(detail) > 0):
            detail = detail[0]
        else:
            detail = 0
        price = re.compile(pricepat, re.S).findall(itemdata)
        if (len(price) > 0):
            price = price[0]
        else:
            price = 0
        commenturl = "https://dsr-rate.tmall.com/list_dsr_info.htm?spuId=1372321809&sellerId=2038648986&groupId&_ksTS=1583569497006_221&callback=jsonp222&itemId="+str(thisid)
        commentdata = urllib.request.urlopen(commenturl).read().decode("utf-8","ignore")
        countpat='"rateTotal":(.*?)'
        count = re.compile(countpat,re.S).findall(commentdata)
        if (len(count) > 0):
            count = count[0]
        else:
            count = 0
        print("-------------------------")
        print("商品名："+str(title))
        print("描述信息："+str(detail))
        print("价格："+str(price))
        print("评论数："+str(count))

