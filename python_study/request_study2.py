# 目标站点：[云栖社区](https://yq.aliyun.com/)
#
# 需求数据：指定关键词的博文数据
#
# 要求：自动翻页并下载到本地

import requests
import re
import time

key = "python"
url = "https://yq.aliyun.com/search/articles/"
data = requests.get(url,params={"q":key}).text
pat1 = '<div class="_search-info">找到(.*?)条关于'
allline=re.compile(pat1,re.S).findall(data)[0]
allpage=int(allline)//15+1
for i in range(0,1):
    print("-------正在爬第"+str(i+1)+"页-------------")
    index=str(i+1)
    getdata={"q":key,
             "p":index,
             }
    data=requests.get(url,params=getdata).text
    pat_url= '<div class="media-body text-overflow">.*?<a href="(.*?)">'
    articles=re.compile(pat_url,re.S).findall(data)
    for j in articles:
        thisurl="https://yq.aliyun.com"+j
        thisdata=requests.get(thisurl).text
        pat_title='<p class="hiddenTitle">(.*?)</p>'
        title=re.compile(pat_title,re.S).findall(thisdata)[0]
        pat_content='<div class="content-detail unsafe markdown-body">(.*?) <div class="copyright-outer-line">'
        content=re.compile(pat_content,re.S).findall(thisdata)[0]
        fh=open("./blog/"+str(title)+str(i)+"_"+str(time.time())+".html","w",encoding="utf-8")
        fh.write(title+"<br /><br />"+content)
        fh.close()