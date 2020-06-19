import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import re


class TextSpider:
    """
    proxies = {'http': 'http://127.0.0.1:10809', 'https': 'http://127.0.0.1:10809'}
    response = requests.get("https://twitter.com/FoVNull/status/1273539944338710529", proxies=proxies)
    soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf-8')
    content = soup.select(".css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    """

    @staticmethod
    def getText() -> str:
        driver = webdriver.Chrome()
        driver.get("https://twitter.com/FoVNull/status/1273539944338710529")
        sleep(3)

        className = "css-901oao r-hkyrab r-1tl8opc r-1blvdjr r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0"
        js = "return document.getElementsByClassName('"+className+"')[0].innerHTML"
        tweet = driver.execute_script(js)
        driver.quit()

        soup = BeautifulSoup(tweet, 'lxml')
        elements = soup.select("span")
        text = ""
        pattern = re.compile(r"[^\x00-\xff]", )
        for e in elements:
            emoji = e.select("img")
            text += e.text
            if len(emoji) > 0:
                text += pattern.search(str(emoji[0])).group()
        return text