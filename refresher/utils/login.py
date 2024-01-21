import time

import requests
from bs4 import BeautifulSoup

from .captcha import CaptchaHandler
from .des import strEnc


class LoginLoader:
    def __init__(self, usr: str, pwd: str) -> None:
        self.x = None
        self.usr = usr
        self.pwd = pwd
        self.captcha_url = None
        self.captcha_path = None
        self.captcha_id = None
        self.login_url = "https://sso.tju.edu.cn/cas/login?service=http%3A%2F%2Fclasses.tju.edu.cn%2Feams%2FhomeExt.action"

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76",
            "Referer": "http://sso.tju.edu.cn/cas/login?service=http%3A%2F%2Fzhjw.tju.edu.cn%2Flogin.jsp",
        }

    def login(self) -> requests.session:
        self.x = requests.session()

        captcha = CaptchaHandler(session=self.x).get_final_captcha()
        res = self.x.get(self.login_url, headers=self.headers)
        soup = BeautifulSoup(res.text, "lxml")

        lt = soup.find(id="lt").get("value")

        execution = soup.select("#loginForm > input[type=hidden]:nth-child(6)")[0]
        if execution is None:
            raise Exception("execution not found")
        execution = execution.get("value")

        rsa = strEnc(self.usr + self.pwd + lt, "1", "2", "3")

        self.x.post(self.login_url, headers=self.headers, data={
            "code": captcha,
            "rsa": rsa,
            "ul": len(self.usr),
            "pl": len(self.pwd),
            "lt": lt,
            "execution": execution,
            "_eventId": "submit",
        })
        self.x.get("http://classes.tju.edu.cn/eams/homeExt.action", headers=self.headers)
        time.sleep(1)
        return self.x
