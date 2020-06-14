import threading
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

from Spider.CtripSpider import CtripSpider


class DispatchSpider(threading.Thread):
    def __init__(self, threadID, begin: int, end: int):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.begin = begin
        self.end = end

    def run(self):
        dispatch(self.begin, self.end, self.threadID)


def writeCSV(infoList: list, location: str, index: int):
    header = ["hotel_id", "comment_num", "useful_num", "pic_num", "comment_date", "rating", "comment"]
    df = pd.DataFrame(data=infoList, columns=header)

    # os.path.exists(location)也行,但没必要@_@
    if index != 13002:
        df.to_csv(location, encoding='utf8', mode='a', header=False, index=False)
    else:
        df.to_csv(location, encoding='utf8', index=False)


def dispatch(begin: int, end: int, threadID):
    keywords = ["图片", "照片"]
    spider = CtripSpider(keywords)
    for i in range(begin, end):  # 范围估计在12000~80000，不过这不太重要，大概就好^_^
        url = "https://hotels.ctrip.com/hotel/" + str(i) + ".html"

        # 校验是否存在该id的酒店
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf-8')
        hotelName = soup.select(".cn_n")
        hotelName = str(hotelName)
        hotelName = hotelName[1:-6]
        flag = hotelName.find(">") == len(hotelName) - 1

        print(threadID, ":", i, "/", end)

        if not flag:
            spider.hotelCommentSpider(url, i)
        if i-begin % 100 and i > begin == 0:
            writeCSV(spider.infoList, "../Resources/comment.csv", i)
            spider.infoList.clear()
    if len(spider.infoList) > 0: writeCSV(spider.infoList, "../Resources/comment.csv", 2)

