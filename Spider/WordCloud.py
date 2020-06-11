import collections
import wordcloud
import matplotlib.pyplot as plt

from Spider.WordCount import WordStatistic


class WordCloud:
    def __init__(self, counter: collections.Counter):
        self.counter = counter

    def drawCloud(self, stopListPath):
        wc = wordcloud.WordCloud(
            scale=10,
            # stopwords=WordStatistic.generateStopSets(stopListPath),
            background_color='white',  # 背景颜色
            width=1000, height=1000,
            font_path='simhei.ttf',
            max_font_size=300,  # 字体大小
            min_font_size=30,
            max_words=len(self.counter)
        )
        wc.generate_from_frequencies(self.counter)  # 从字典生成词云
        # self.wc.to_file('test.png')  # 图片保存
        plt.figure('test')  # 图片显示的名字
        plt.imshow(wc)
        plt.axis('off')  # 关闭坐标
        plt.show()

