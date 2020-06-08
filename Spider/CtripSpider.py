from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep


def hotelCommentSpider(url: str) -> list:
    res = []
    driver = webdriver.Ie()
    driver.get(url)

    # 启动控制台，用来debug js
    # builder = ActionChains(driver)
    # builder.key_down(Keys.F12).perform()

    # 这个不知道为什么没用，以后再研究
    # js = "document.getElementById(\"J_searchInput\").value =\"2\";document.getElementById(\"J_searchResultBtn\").click();"

    # 规范js代码见 Resources/test.js

    sleep(2)
    arg = "图片"
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
        data = driver.find_element_by_class_name("comment_detail_list")
        strs = str(data.text).split("\n")
        for i in range(len(strs)):
            if strs[i].__contains__("发表于2"): res.append(strs[i - 1])
        try:
            driver.execute_script(page_js)
            sleep(2)
        except JavascriptException as e:
            break
    # driver.quit()
    return res


if __name__ == '__main__':
    map = {}
    for i in range(441351, 441352):  # 范围估计在13000~80000，不过这不太重要@_@
        url = "https://hotels.ctrip.com/hotel/"+str(i)+".html"
        value = hotelCommentSpider(url)
        if len(value) > 0: map[i] = value