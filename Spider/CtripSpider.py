from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd


def hotelCommentSpider(url: str, id: int):
    driver = webdriver.Ie()
    driver.get(url)

    # 启动控制台，用来debug js
    # builder = ActionChains(driver)
    # builder.key_down(Keys.F12).perform()

    # 这个不知道为什么没用，以后再研究
    # js = "document.getElementById(\"J_searchInput\").value =\"2\";document.getElementById(\"J_searchResultBtn\").click();"

    # 规范js代码见 Resources/test.js

    sleep(2)
    arg = "入住"
    search_js = 'window.document.__webdriver_script_fn = ' \
         '(function () {' \
         'document.getElementById("J_searchInput").value = "' + arg + '";' \
         'document.getElementById("J_searchResultBtn").click();' \
         '})();'
    driver.execute_script(search_js)

    sleep(2)
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
                cMap["date"] = s[3:]
                cMap["comment"] = strs[i - 1]
                if strs[i - 2].__contains__("分"): cMap["rating"] = strs[i - 2][0:3]
                infoList.append(cMap)
                cMap = {"hotel_id": id}
        try:
            driver.execute_script(page_js)
            sleep(2)
        except JavascriptException as e:
            break
    driver.quit()


def writeCSV():
    header = ["hotel_id", "comment_num", "useful_num", "pic_num", "date", "rating", "comment"]
    df = pd.DataFrame(data=infoList, columns=header)
    print(df)
    df.to_csv("Resources/comment.csv", encoding='utf8')


infoList = []
if __name__ == '__main__':
    for i in range(441351, 441352):  # 范围估计在13000~80000，不过这不太重要@_@
        url = "https://hotels.ctrip.com/hotel/"+str(i)+".html"
        hotelCommentSpider(url, i)

    writeCSV()