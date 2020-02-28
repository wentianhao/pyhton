import requests
import re

hd = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
px = {"http":"http://127.0.0.1:8888"}


rst = requests.get("https://www.aliwx.com.cn/",headers=hd,proxies=px)
print(rst)
title = re.compile("<title>(.*?)</title>",re.S).findall(rst.text)
print(title)

pr = {"wd":"阿里文学"}
rst2 = requests.get("http://www.baidu.com/s",params=pr)
print(rst2)

print(rst2.text)
print(rst2.content)
print(rst2.encoding)
print(rst2.url)
print(rst2.status_code)

cookie  = requests.utils.dict_from_cookiejar(rst2.cookies)
print(cookie)

postdata = {"name":"www","pass":"123"}
rst3 = requests.post("https://www.iqianyue.com/mypost/",data=postdata)
print(rst3.text)