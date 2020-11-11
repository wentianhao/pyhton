import smtplib
import requests
import json
from email.mime.text import MIMEText
import time,datetime
import schedule

# 得到天气
def get_sky(city):
    url='https://free-api.heweather.net/s6/weather/now?location='+city+'&key=8a92371afde5490c9ecf3e9346ff189a'
    r = requests.get(url)
    now = json.loads(r.text)
    # print(now)
    a = now['HeWeather6'][0]['basic']
    b = now['HeWeather6'][0]['now']
    c = now['HeWeather6'][0]['update']
    data = []
    title = ''
    title += c['loc']
    title += ' ' + a['location']
    title += ' ' + b['cond_txt']
    title += '  温度: %s℃' % (b['tmp'])
    data.append(title)
    station = ''
    station += "省份：%s<br>"%a['admin_area']
    station += '城市：%s<br>'%(a['location'])
    station += '时间：%s<br>'%(c['loc'])
    station += '温度: %s℃<br>' % (b['tmp'])
    station += '天气: %s<br>'%(b['cond_txt'])
    station += '体感温度: %s℃<br>' % (b['fl'])
    station += '云量: %s<br>' % (b['cloud'])
    station += '能见度: %s<br>' % (b['vis'])
    station += '风力: %s<br>' % (b['wind_sc'])
    station += '风向: %s<br>' % (b['wind_dir'])
    data.append(station)
    # print(station)
    return data

# 邮件传输
def smtp_tran(data,t0):
    # print(data)
    t = data[0]
    weather = data[1]
    # print(t)
    # print(time)
    msg = MIMEText(weather,'html','utf-8')
    HOST = 'smtp.qq.com'
    server = smtplib.SMTP_SSL(HOST, 465)
    server.set_debuglevel(1)
    SUBJECT = t
    FROM = 'xxxxxxx@qq.com'
    server.login(FROM, 'xxxxx')
    TO = t0
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    for to in TO:
        # print(to)
        try:
            msg['To'] = to
            # print(to)
            server.sendmail(FROM, [to], msg.as_string())
            time.sleep(10)
            now_time = datetime.datetime.now()
            print(str(now_time) + ' 成功发送给%s' % (to))
        except Exception as e:
            print("error:",e)
            continue
    server.quit()

def job():
    smtp_tran(get_sky('wuhan'), ['xxxxxx@qq.com', 'xxxxxxx@qq.com'])

schedule.every().day.at("07:00").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)