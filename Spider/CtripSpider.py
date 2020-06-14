from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep


class CtripSpider:
    def __init__(self, keywords):
        self.infoList = []
        self.args = keywords

    def hotelCommentSpider(self, url: str, id: int):
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

