from typing import Union
import requests
import os


class SignIn(object):
    def __init__(self, username: str, password: str):
        """
        自动登录类，包含获取登录信息方法、签到方法、保存登录信息方法、加载登录信息方法
        """
        self.username = username
        self.password = password
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78"
        }
        self.cookies = self.loadData() if os.path.exists("user.txt") else self.getCookie()

    def getCookie(self) -> Union[int, str, float]:
        """
        用于获取用户登录信息
        :return: 包含登录信息列表
        """
        data = {
            "username": self.username,
            "password": self.password
        }
        cookie = {}
        url = "https://fishc.com.cn/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes"
        try:
            cookiesJar = requests.post(url=url, data=data, headers=self.headers).cookies
            cookie = requests.utils.dict_from_cookiejar(cookiesJar)
            self.saveData(cookie)
        except:
            return 1

        return cookie

    def autoSign(self) -> None:
        """
        发起签到请求
        :return: 打印提示语句
        """
        url = "https://fishc.com.cn/plugin.php?id=k_misign:sign"

        html = requests.get(url=url, headers=self.headers, cookies=self.cookies).text

        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "lxml")
        try:
            a = soup.find_all(name="a", id="JD_sign")[0]
            a_href = "https://fishc.com.cn/" + a.get("href")
            requests.get(url=a_href, headers=self.headers, cookies=self.cookies)
            print("签到完成~真棒")
        except:
            print("你今天已经签到过了哦~\n明天再来吧~")

    def saveData(self, cookie: dict) -> None:
        """
        将用户登录信息保存
        :param cookie: 保存登录信息
        :return: 无
        """
        with open("user.txt", "w+") as f:
            cookie = str(cookie)
            readlines = f.readlines()
            if cookie not in readlines:
                f.write(cookie)

    def loadData(self) -> dict:
        """
        加载登录信息（如果存在）
        :return: 无
        """
        with open("user.txt", "r") as f:
            readline = f.readline()
            import ast
            data = ast.literal_eval(readline)
            return data


def main() -> None:
    """主方法，程序运行逻辑"""
    # 来个小彩蛋 >x<
    fishc = """
     ________  ___      ________       ___  ___      ________     
    |\  _____\|\  \    |\   ____\     |\  \|\  \    |\   ____\     
    \ \  \__/ \ \  \   \ \  \___|_    \ \    \  \   \ \  \___|     
     \ \   __\ \ \  \   \ \_____  \    \ \   __  \   \ \  \        
      \ \  \_|  \ \  \   \|____|\  \    \ \  \ \  \   \ \  \____   
       \ \__\    \ \__\    ____\_\  \    \ \__\ \__\   \ \_______\ 
        \|__|     \|__|   |\_________\    \|__|\|__|    \|_______|
                          \|_________|                             
    
>>> 欢迎使用，程序启动中...
>>> 初始化成功！
    """
    print(fishc)
    username = input(">>> 请输入用户名：")
    password = input(">>> 请输入密码：")
    sign = SignIn(username=username, password=password)
    if sign.cookies == 1:
        print("登录失败！检查一下账号密码，还有网络状态哦~")
    else:
        sign.autoSign()


if __name__ == '__main__':
    main()
