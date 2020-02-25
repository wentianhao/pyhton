from urllib.parse import urlparse

import requests
import time
from bs4 import BeautifulSoup
from requests import HTTPError

timeout = 3
headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-us",
           "Connection": "keep-alive",
           "Accept-Charset": "GB2312,utf-8;q=0.7,*;q=0.7"}


def extract_host(url: str) -> str:
    parse = urlparse(url)
    if parse.netloc == "":
        return None
    else:
        return parse.netloc



def filter_url(urls,host):
    newlist = []
    for i in urls:
        try:
            url = i['href']
            if "http:" in url or "https:" in url:
                newlist.append(url)
            else:
                newlist.append("http://"+host+url)
        except KeyError as err:
            continue
    return newlist


def extract_info(url: str) -> str:
    host = extract_host(url)
    if host is not None:
        headers['Host'] = host

    try:
        r = requests.get(url, timeout=timeout, headers=headers)
        r.raise_for_status()  # 判断状态
        r.encoding = r.apparent_encoding
        obj = BeautifulSoup(r.text, "lxml")
        title = obj.head.title.get_text()
        urls = filter_url(obj.find_all('a'),host)
        return title,urls
    except HTTPError as e:
        return str(e.args).split(":")[0]


def extract_title(url: str) -> str:
    host = extract_host(url)
    if host is not None:
        headers['Host'] = host

    try:
        r = requests.get(url, timeout=timeout, headers=headers)
        r.raise_for_status()  # 判断状态
        r.encoding = r.apparent_encoding
        obj = BeautifulSoup(r.text, "lxml")
        title = obj.head.title.get_text()
        return f"{title} : {url}"
    except HTTPError as e:
        return str(e.args).split(":")[0]


def get_item_form_url(url: str):
    title,urls = extract_info(url)
    print(f"{title} : {url}")
    for i in urls:
        try:
            print(extract_title(i))
            # print("Sleep 1 Second")
            # time.sleep(1)
            # print("Finish")
        except Exception:
            continue
    


if __name__ == '__main__':
    while True:
        url_test = "https://baike.baidu.com/item/%E6%B4%9B%E5%A4%A9%E4%BE%9D"
        get_item_form_url(url_test)
        break
