import urllib.request
import re

cid = "0"

for i in range(0,100):
    print("第"+str(i+1)+"页的评论数据")
    url = "https://video.coral.qq.com/varticle/4831064204/comment/v2?callback=_varticle4831064204commentv2&orinum=10&oriorder=o&pageflag=1&cursor=" + str(
        cid) + "&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=132&_=1582873152540"
    data = urllib.request.urlopen(url).read().decode("utf-8","ignore")
    pat = '"content":"(.*?)"'
    comments = re.compile(pat,re.S).findall(data)
    for item in comments:
        print(str(item))
        print("------------------")
    pat2 = '"last":"(.*?)"'
    cid = re.compile(pat2,re.S).findall(data)[0]