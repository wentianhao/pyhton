import requests
from lxml import etree
import logging
import os
# 网易云音乐飙升榜
url = 'https://music.163.com/discover/toplist'
hd = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger('download_music')
download_dir = 'music/'

def get_top_ids():
    r = requests.get(url,headers=hd)
    html = etree.HTML(r.text)
    nodes = html.xpath("//ul[@class='f-cb']/li")
    logger.info('{}  {}'.format('榜单 ID', '榜单名称'))
    ans = dict()
    for node in nodes:
        id = node.xpath('./@data-res-id')[0]
        name = node.xpath("./div/p[@class='name']/a/text()")[0]
        ans[id] = name
        logger.info('{}  {}'.format(id, name))
    return ans

def get_topic_songs(topic_id,topic_name):
    params={"id":topic_id}
    r = requests.get(url,params=params,headers=hd)
    html = etree.HTML(r.text)
    nodes = html.xpath("//ul[@class='f-hide']/li")
    ans = dict()
    logger.info('{} 榜单 {} 共有歌曲 {} 首 {}'.format('*' * 10, topic_name, len(nodes), '*' * 10))
    for node in nodes:
        id = node.xpath('./a/@href')[0].split('=')[1]
        name = node.xpath('./a/text()')[0]
        ans[id] = name
        logger.info('{} {}'.format(id,name))
    return ans

def down_song_by_song_id_name(id,name):
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)
    url = 'http://music.163.com/song/media/outer/url?id={}.mp3'
    r = requests.get(url.format(id),headers=hd)
    is_fail = False
    try:
        with open(download_dir+name+'.mp3','wb') as f:
            f.write(r.content)
    except:
        is_fail = True
        logger.info("%s 下载出错" %name)
    if not is_fail:
        logger.info("%s 下载完成" %name)

def down_song_by_topic_id(id,name):
    ans = get_topic_songs(id, ids[id])
    for id ,name in ans.items():
        down_song_by_song_id_name(id,name)

if __name__ == '__main__':
    ids = get_top_ids()
    while True:
        print('')
        logger.info('输入 Q 退出程序')
        logger.info('输入 A 下载全部榜单歌曲')
        logger.info('输入榜单 Id 下载当前榜单歌曲')

        id = input('请输入：')

        if str(id) == 'Q':
            break
        elif str(id) == 'A':
            for id in ids:
                down_song_by_topic_id(id, ids[id])
        else:
            print('')
            ans = get_topic_songs(id, ids[id])
            print('')
            logger.info('输入 Q 退出程序')
            logger.info('输入 A 下载全部歌曲')
            logger.info('输入歌曲 Id 下载当前歌曲')
            id = input('请输入：')
            if str(id) == 'Q':
                break
            elif id == 'A':
                down_song_by_topic_id(id, ans[id])
            else:
                down_song_by_song_id_name(id, ans[id])
