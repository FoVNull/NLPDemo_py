from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import os


# 后续更新：https://github.com/FoVNull/NLPDemo_py/tree/master/Spider
class CtripSpider:
    def __init__(self, keywords):
        self.infoList = []
        self.args = keywords

    def hotelCommentSpider(self, url: str, id: int) -> list:
        driver = webdriver.Ie()
        driver.set_window_size(0, 0)
        driver.set_window_position(1300, 100)
        driver.get(url)

        # 启动控制台，用来debug js
        # builder = ActionChains(driver)
        # builder.key_down(Keys.F12).perform()

        # 规范js代码见 Resources/test.js

        search_js_list = self.mergeJS(self.args)
        for search_js in search_js_list:
            sleep(1)
            try:
                driver.execute_script(search_js)
            except JavascriptException:
                break
            sleep(1)
            self.simulateOperation(driver, id)
            driver.refresh()

        driver.quit()
        return self.infoList

    def mergeJS(self, args) -> list:
        js = []
        # 这个不知道为什么没用，以后再研究
        # js = "document.getElementById(\"J_searchInput\").value =\"2\";document.getElementById(\"J_searchResultBtn\").click();"
        for arg in args:
            search_js = 'window.document.__webdriver_script_fn = ' \
                        '(function () {' \
                        'document.getElementById("J_searchInput").value = "' + arg + '";' \
                        'document.getElementById("J_searchResultBtn").click();' \
                        '})();'
            js.append(search_js)
        return js

    def simulateOperation(self, driver, id):
        # 搜索后的结果需要点下一页而不能直接输入页码跳转，应该是携程的bug
        page_js = 'window.document.__webdriver_script_fn = ' \
                  '(function() {' \
                  'document.getElementsByClassName("c_down")[0].click();' \
                  '})();'
        while True:
            cMap = {"hotel_id": id}
            data = driver.find_element_by_class_name("comment_detail_list")
            strs = str(data.text).split("\n")
            for i in range(len(strs)):
                s = strs[i]
                if s.__contains__("点评总数"):
                    cMap["comment_num"] = s[4:]
                if s.__contains__("被点有用"):
                    cMap["useful_num"] = s[4:]
                if s.__contains__("上传图片"):
                    cMap["pic_num"] = s[4:]
                if s.__contains__("发表于2"):
                    cMap["comment_date"] = s[3:]
                    j = i
                    if strs[i - 1] == "查看更多": j -= 1
                    cMap["comment"] = strs[j - 1]
                    if strs[j - 2].__contains__("分"):cMap["rating"] = strs[j - 2][0:3]
                    self.infoList.append(cMap)
                    cMap = {"hotel_id": id}
            try:
                driver.execute_script(page_js)
                sleep(1)
            except JavascriptException as e:
                break


def writeCSV(infoList: list, location: str, index: int):
    header = ["hotel_id", "comment_num", "useful_num", "pic_num", "comment_date", "rating", "comment"]
    df = pd.DataFrame(data=infoList, columns=header)

    # os.path.exists(location)也行,但没必要@_@
    if index != 13002:
        df.to_csv(location, encoding='utf8', mode='a', header=False, index=False)
    else:
        df.to_csv(location, encoding='utf8', index=False)


def dropDuplicates(path: str):
    df = pd.read_csv(path + "/comment.csv")
    df.drop_duplicates(inplace=True)
    df.to_csv(path + "/comment_1.csv", encoding='utf8', index=False)


if __name__ == '__main__':
    keywords = ["图片", "照片"]
    spider = CtripSpider(keywords)
    count = 0
    # 16100
    for i in range(15600, 16000):  # 范围估计在12000~80000，不过这不太重要，大概就好^_^
        url = "https://hotels.ctrip.com/hotel/"+str(i)+".html"

        # 校验是否存在该id的酒店
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf-8')
        hotelName = soup.select(".cn_n")
        hotelName = str(hotelName)
        hotelName = hotelName[1:-6]
        flag = hotelName.find(">") == len(hotelName) - 1

        if not flag:
            spider.hotelCommentSpider(url, i)
            size = len(spider.infoList)
            if i%100 == 0:
                writeCSV(spider.infoList, "./Resources/comment.csv", i)
                spider.infoList.clear()
            if size != count:
                count = size; print(count, end=" ==>  ")
        print(str(i)+"/20000")
    if len(spider.infoList) > 0: writeCSV(spider.infoList, "./Resources/comment.csv", 2)