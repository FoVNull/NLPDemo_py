import pandas as pd

from Spider.DispatchSpider import DispatchSpider


def dropDuplicates(path: str):
    df = pd.read_csv(path + "/comment.csv")
    df.drop_duplicates(inplace=True)
    df.to_csv(path + "/comment_1#.csv", encoding='utf8', index=False)


if __name__ == '__main__':
    # 每个线程的爬取条数不小于100条，因为我在爬虫中设定每百条写入一次文件
    threadCapacity = 1000
    for i in range(5):
        begin = 20001 + i * threadCapacity
        dispather = DispatchSpider(i, begin, begin + threadCapacity)
        dispather.start()