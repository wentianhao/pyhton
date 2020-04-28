import requests
import re
import json
import time
import jieba
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud

# 请求爱奇艺评论接口，返回response信息
def getMovieinfo(url):
    '''
    请求爱奇艺评论接口，返回response信息
    参数url：评论的url
    :return:
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    response = requests.get(url, headers=headers,verify=False)
    return response.text

# 解析json数据，获取评论
def saveMovieInfoToFile(lastId,arr):
    '''
    解析json数据，获取评论
    参数  lastId:最后一条评论ID  arr:存放文本的list
    :return: 新的lastId
    :return:
    '''
    url = 'https://sns-comment.iqiyi.com/v3/comment/get_comments.action?agent_type=118&business_type=17&content_id=15068699100&last_id='
    url = url + str(lastId)
    responseText = getMovieinfo(url)
    responseJson = json.loads(responseText)
    comments = responseJson['data']['comments']
    for comment in comments:
        if 'content' in comment.keys():
            print(comment['content'])
            arr.append(comment['content'])
        lastId = str(comment['id'])
    return lastId


# 去除文本中特殊字符
def clear_special_char(content):
    '''
    正则处理特殊字符
    参数 content:原文本
    return: 清除后的文本
    '''
    # 过滤除中英文及数字以外的其他字符
    res = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
    s = res.sub(r'', content)
    return s


def fenci(text):
    '''
    利用jieba进行分词
    参数 text:需要分词的句子或文本
    return：分词结果
    '''
    jieba.load_userdict('add_words.txt')
    seg = jieba.lcut(text,cut_all=False)
    return seg


def stopwordslist(filePath):
    '''
    创建停用词表
    参数 file_path:停用词文本路径
    return：停用词list
    '''
    stopwords = [line.strip() for line in open(filePath,encoding='utf-8').readlines()]
    return stopwords


def movestopwords(words,stopwords,counts):
    '''
    去除停用词,统计词频
    参数 file_path:停用词文本路径 stopwords:停用词list counts: 词频统计结果
    return：None
    '''
    out = []
    for word in words:
        if word not in stopwords:
            if len(word) != 1:
                counts[word] = counts.get(word, 0) + 1
    print(counts)
    return None

def drawcounts(counts,num):
    '''
    绘制词频统计表
    参数 counts: 词频统计结果 num:绘制topN
    return：none
    '''
    x = []
    y = []
    c_order = sorted(counts.items(),key=lambda a:a[1],reverse=True)
    print(c_order)
    for c in c_order[:num]:
        x.append(c[0])
        y.append(c[1])

    print(x,y)
    # 设置显示中文
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体

    plt.bar(x,y)
    plt.title("词频统计结果")
    plt.show()

def drawcloud(counts):
    '''
    根据词频绘制词云图
    参数 words:统计出的词频结果
    return：none
    '''
    # cloud_mask = imageio.imread('mask.png')
    cloud_mask = np.array(Image.open('mask.png'))
    st = (["真的","东西"])

    wc = WordCloud(background_color='white',
                   mask=cloud_mask,
                   max_words=150,
                   font_path='simhei.ttf',
                   min_font_size=10,
                   max_font_size=100,
                   width=400,
                   relative_scaling=0.3,
                   stopwords=st)
    wc.fit_words(counts)
    wc.to_file('pic.png')


def text_detection(text,file_path):
    '''
    使用hub对评论进行内容分析
    return：分析结果
    '''





if __name__ == "__main__":
    n = 10
    lastId = ''
    arr = []
    with open('aqy.txt','a',encoding='UTF-8') as f:
        for i in range(n):
            lastId = saveMovieInfoToFile(lastId,arr)
            time.sleep(0.5)
        for item in arr:
            clearItem = clear_special_char(item)
            f.write(clearItem+'\n')
    print("共爬取"+str(len(arr))+"条评论")

    fp = open('aqy.txt','r',encoding='UTF-8')
    counts = {}

    for line in fp:
        words = fenci(line)
        stopwords = stopwordslist('stop.txt')
        movestopwords(words,stopwords,counts)
    drawcounts(counts,10)
    drawcloud(counts)

