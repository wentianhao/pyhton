import re
import os
import json

import requests

"""
@Author  :   猪哥,
@Version :   2.0"
"""

s = requests.Session()
# cookies序列化文件
COOKIES_FILE_PATH = 'taobao_login_cookies.txt'


class UsernameLogin:

    def __init__(self, username, ua, TPL_password2):
        """
        账号登录对象
        :param username: 用户名
        :param ua: 淘宝的ua参数
        :param TPL_password2: 加密后的密码
        """
        # 检测是否需要验证码的URL
        self.user_check_url = 'https://login.taobao.com/member/request_nick_check.do?_input_charset=utf-8'
        # 验证淘宝用户名密码URL
        self.verify_password_url = "https://login.taobao.com/member/login.jhtml"
        # 访问st码URL
        self.vst_url = 'https://login.taobao.com/member/vst.htm?st={}'
        # 淘宝个人 主页
        self.my_taobao_url = 'http://i.taobao.com/my_taobao.htm'

        # 淘宝用户名
        self.username = username
        # 淘宝关键参数，包含用户浏览器等一些信息，很多地方会使用，从浏览器或抓包工具中复制，可重复使用
        self.ua = ua
        # 加密后的密码，从浏览器或抓包工具中复制，可重复使用
        self.TPL_password2 = TPL_password2

        # 请求超时时间
        self.timeout = 3

    def _user_check(self):
        """
        检测账号是否需要验证码
        :return:
        """
        data = {
            'username': self.username,
            'ua': self.ua
        }
        try:
            response = s.post(self.user_check_url, data=data, timeout=self.timeout)
            response.raise_for_status()
        except Exception as e:
            print('检测是否需要验证码请求失败，原因：')
            raise e
        needcode = response.json()['needcode']
        print('是否需要滑块验证：{}'.format(needcode))
        return needcode

    def _verify_password(self):
        """
        验证用户名密码，并获取st码申请URL
        :return: 验证成功返回st码申请地址
        """
        verify_password_headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://login.taobao.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fi.taobao.com%2Fmy_taobao.htm%3Fnekot%3Dd2luZG93c7a61583591116672',
        }
        # 登录toabao.com提交的数据，如果登录失败，可以从浏览器复制你的form data
        verify_password_data = {
            'TPL_username': self.username,
            'ncoToken': '0bb97e50513ee7108fe3ee98ef4fd0d7dbb73e42',
            'slideCodeShow': 'false',
            'useMobile': 'false',
            'lang': 'zh_CN',
            'loginsite': 0,
            'newlogin': 0,
            'TPL_redirect_url': 'https://i.taobao.com/my_taobao.htm?nekot=d2luZG93c7a61583591116672',
            'from': 'tb',
            'fc': 'default',
            'style': 'default',
            'keyLogin': 'false',
            'qrLogin': 'true',
            'newMini': 'false',
            'newMini2': 'false',
            'loginType': '3',
            'gvfdcname': '10',
            'gvfdcre': '68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D61317A30322E312E3735343839343433372E372E65383061373832645570316C767626663D746F70266F75743D7472756526726564697265637455524C3D6874747073253341253246253246692E74616F62616F2E636F6D2532466D795F74616F62616F2E68746D2533466E656B6F7425334464326C755A4739336337613631353833353931313136363732',
            'TPL_password_2': self.TPL_password2,
            'loginASR': '1',
            'loginASRSuc': '1',
            'oslanguage': 'zh-CN',
            'sr': '1536*864',
            'naviVer': 'chrome|79.0394588',
            'osACN': 'Mozilla',
            'osAV': '5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'osPF': 'Win32',
            'appkey': '00000000',
            'mobileLoginLink': 'https://login.taobao.com/member/login.jhtml?redirectURL=https://i.taobao.com/my_taobao.htm?nekot=d2luZG93c7a61583591116672&useMobile=true',
            'showAssistantLink': '',
            'um_token': 'T842EFDB3839632D70BEE88EF790875973CEE81ADB24A76C9228DF5B86D',
            'ua': self.ua
        }
        try:
            response = s.post(self.verify_password_url, headers=verify_password_headers, data=verify_password_data,
                              timeout=self.timeout)
            response.raise_for_status()
            # 从返回的页面中提取申请st码地址
        except Exception as e:
            print('验证用户名和密码请求失败，原因：')
            raise e
        # 提取申请st码url
        apply_st_url_match = re.search(r'<script src="(.*?)"></script>', response.text)
        # 存在则返回
        if apply_st_url_match:
            print('验证用户名密码成功，st码申请地址：{}'.format(apply_st_url_match.group(1)))
            return apply_st_url_match.group(1)
        else:
            raise RuntimeError('用户名密码验证失败！response：{}'.format(response.text))

    def _apply_st(self):
        """
        申请st码
        :return: st码
        """
        apply_st_url = self._verify_password()
        try:
            response = s.get(apply_st_url)
            response.raise_for_status()
        except Exception as e:
            print('申请st码请求失败，原因：')
            raise e
        st_match = re.search(r'"data":{"st":"(.*?)"}', response.text)
        if st_match:
            print('获取st码成功，st码：{}'.format(st_match.group(1)))
            return st_match.group(1)
        else:
            raise RuntimeError('获取st码失败！response：{}'.format(response.text))

    def login(self):
        """
        使用st码登录
        :return:
        """
        # 加载cookies文件
        if self._load_cookies():
            return True
        # 判断是否需要滑块验证
        self._user_check()
        st = self._apply_st()
        headers = {
            'Host': 'login.taobao.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        try:
            response = s.get(self.vst_url.format(st), headers=headers)
            response.raise_for_status()
        except Exception as e:
            print('st码登录请求，原因：')
            raise e
        # 登录成功，提取跳转淘宝用户主页url
        my_taobao_match = re.search(r'top.location.href = "(.*?)"', response.text)
        if my_taobao_match:
            print('登录淘宝成功，跳转链接：{}'.format(my_taobao_match.group(1)))
            self._serialization_cookies()
            return True
        else:
            raise RuntimeError('登录失败！response：{}'.format(response.text))

    def _load_cookies(self):
        # 1、判断cookies序列化文件是否存在
        if not os.path.exists(COOKIES_FILE_PATH):
            return False
        # 2、加载cookies
        s.cookies = self._deserialization_cookies()
        # 3、判断cookies是否过期
        try:
            self.get_taobao_nick_name()
        except Exception as e:
            os.remove(COOKIES_FILE_PATH)
            print('cookies过期，删除cookies文件！')
            return False
        print('加载淘宝登录cookies成功!!!')
        return True

    def _serialization_cookies(self):
        """
        序列化cookies
        :return:
        """
        cookies_dict = requests.utils.dict_from_cookiejar(s.cookies)
        with open(COOKIES_FILE_PATH, 'w+', encoding='utf-8') as file:
            json.dump(cookies_dict, file)
            print('保存cookies文件成功！')

    def _deserialization_cookies(self):
        """
        反序列化cookies
        :return:
        """
        with open(COOKIES_FILE_PATH, 'r+', encoding='utf-8') as file:
            cookies_dict = json.load(file)
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            return cookies

    def get_taobao_nick_name(self):
        """
        获取淘宝昵称
        :return: 淘宝昵称
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        try:
            response = s.get(self.my_taobao_url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print('获取淘宝主页请求失败！原因：')
            raise e
        # 提取淘宝昵称
        nick_name_match = re.search(r'<input id="mtb-nickname" type="hidden" value="(.*?)"/>', response.text)
        if nick_name_match:
            print('登录淘宝成功，你的用户名是：{}'.format(nick_name_match.group(1)))
            return nick_name_match.group(1)
        else:
            raise RuntimeError('获取淘宝昵称失败！response：{}'.format(response.text))


if __name__ == '__main__':
    # 淘宝用户名
    username = 'windows逗'
    # 淘宝重要参数，从浏览器或抓包工具中复制，可重复使用
    ua = ua = '122#FeDzIDjDEEx1z4pZMEpJEJponDJE7SNEEP7rEJ+/f9t/2oQLpo7iEDpWnDEeK51HpyGZp9hBuDEEJFOPpC76EJponDJL7gNpEPXZpJRgu4Ep+FQLpoGUEJLWn4yP7SQEEyuLpERPWSmyprZCnaRx9kbN1ojjDgnNi1ejROuSgORvgdza6pHY5m7AyRd4yEFXAU5O+/1R03AnZKot+1HGXnRk+DKQ9pyCV6XYsJGDqMfpYzrg+NXXuOIEDeRF1ygVdNbbyFfmqMf2ENpC3VDb5y0EDLXT8BLUJNI9UV4n7W3bD93xnSL1elWEELXZ8oL6JNEEyBfDqMAbEEpangL4ul0EDLVr8opUJ4bEyF3mqWivDEpx7S11uO0EoL34HBWHun8bA07Nnz0L6/oYbSR81PMFGbTJmT43UYAG/gs6QC9SGrSIQbBp9Mu4Nhb3HAkFFci0BO8nV0hR8Yco3a2Ph4wmYvRDIIFfQdpWo7x4/+kMSFQiAVg+EArJd3t23gJMF6Q9Z+X2Xq2rqsI0DVNXdnj4gzDPCuySWHOaWxaMKIVIC+rjzsQc/dQKHMJ2ILBPi771aqCShuDuwPnAENL6YgVR1qtKSvxzTLIViUnf0QXyktIgDBCxjnTncHVMiIvBAN9jUOlSyRfawj9a8ucXLcqjfMm5KkKZJjFlZTnk1GKznlc7qIctWGyMEI+iPeWL/JAEI/RBqgEYh51EzAciR6vy4mU1yv5WW3pIC44CMGdQyez01jbuqdL0HObreaZZbgWc21bC+1jfBdiSNUHo+oCs5tPyXANFduYenN2oNntcFrsEo49wI1js7Q+Bm1WyWTICp/xU36OtR+pqgarysfYWLl2DoDvPITxxMcZN8eIjc5E5XHdz/wAoNjA9IkvIq9F74Z5m1IkBYCEMRy8i0mYQINa0BXBR1YkEUeUpRMGZ/qTtfUwk83wX3PvbtjyPfhp/OKCywMGKNhx6Vpceh0ggJXSaUSDNmcDv2FFzbGWfO+w5S0ur6HV2Ct0hUglwmiTkTcWkUQI7G2LyXxhsv1p00+eBIHkPLpgq3QuXks2IzFHcoroPgVObJtEt6sz9g2OTlNlEeFP4nnpzjyJX7YQ8mdzAWLysdzIlqppn+hkLADfJWl3Ynp2iJLW4Dw5+e+vvxTSKO8+LYPZob+d5nfebj1LpcZmUR5Cgh1Ls+uY6meffcqa2Zsf5e552a5ILCCXQfb8KD/7mZuLdt1tE6sfZlMSVWZMRFaLS/4=='
    # 加密后的密码，从浏览器或抓包工具中复制，可重复使用
    TPL_password2 = '6233d4a1c3c1bb692aa0b488fcf93a88db8872f364f346d4e6de3bb71be6a10e00e6e66332eb52db927c16749cded44568c7b8d4371bd02e4de29ec453b4ed052e9b17c3e5f45b1ae760d7c9e59ec79057b12990b4a256af0b18562a5d0655e52b7acdf9abf928ce3aa0b9682c03d0c93f0174f6a7f648a839847c0c3f7bb376'
    ul = UsernameLogin(username, ua, TPL_password2)
    ul.login()
