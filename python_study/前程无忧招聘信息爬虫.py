import re
import requests

url = "https://search.51job.com/list/180000,000000,0000,00,9,99,python,2,1.html"

hd={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}

response = requests.get(url,headers=hd)
# 如果网页出现乱码，通传编码方式
data = bytes(response.text,response.encoding).decode("gbk","ignore")
# print(len(data))
pat_pag = "共(.*?)条职位"
allline = re.compile(pat_pag,re.S).findall(data)[0]
# print(allline)
allpage = int(allline)//50 + 1

for i in range(0,2):
    print("------------正在爬"+str(i+1)+"页---------")
    url = "https://search.51job.com/list/180000,000000,0000,00,9,99,python,2,"+str(i+1)+".html"
    # print(url)
    response = requests.get(url, headers=hd)
    # 如果网页出现乱码，通传编码方式
    thisdata = bytes(response.text, response.encoding).decode("gbk", "ignore")
    # print(thisdata)
    job_url_pat='<em class="check" name="delivery_em" onclick="checkboxClick.this."></em>.*?href="(.*?).html'
    job_url_all = re.compile(job_url_pat,re.S).findall(thisdata)
    # print(len(job_url_all))
    for job_url in job_url_all:
        # print(job_url)
        thisurl=job_url+".html"
        response=requests.get(thisurl)
        thisdata=bytes(response.text,response.encoding).decode("gbk","ignore")
        pat_title='<h1 title="(.*?)"'
        pat_company='<p class="cname">.*?title="(.*?)"'
        pat_money='</h1><strong>(.*?)</strong>'
        pat_addr='上班地址：</span>(.*?)</p>'
        title = re.compile(pat_title,re.S).findall(thisdata)[0]
        company = re.compile(pat_company,re.S).findall(thisdata)[0]
        money = re.compile(pat_money,re.S).findall(thisdata)[0]
        try:
            addr = re.compile(pat_addr,re.S).findall(thisdata)[0]
        except IndexError:
            addr = "空"

        print("-------------------")
        print(title)
        print(company)
        print(money)
        print(addr)
