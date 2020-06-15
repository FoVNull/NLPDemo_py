import collections #import Counter
import numpy as np
import wordcloud
from PIL import Image # 图像处理库
import matplotlib.pyplot as plt # 图像展示库
import pandas as pd
fr = open('D:\StanceDetection\LDA_test\output/2018标题_jieba.txt', 'r', encoding='utf-8')
b=[]
for line in fr.readlines():
    str_list = line.split()
    #print(str_list)
    for i in range(len(str_list)):
        b.append(str_list[i])
word_counts = collections.Counter(b)
#print(word_counts)
#
#mask = np.array(Image.open('xin.jpg'))  # 定义词频背景
wc = wordcloud.WordCloud(
    font_path='simhei.ttf',  # 字体路劲
    background_color='white',  # 背景颜色
    width=1000,
    height=1000,
    max_font_size=300,  # 字体大小
    min_font_size=50,
    # mask=plt.imread('xin.jpg'),  # 背景图片
    max_words=20#len(word_counts)
)

wc.generate_from_frequencies(word_counts)  # 从字典生成词云
wc.to_file('2018标题.png')  # 图片保存
plt.figure('2018标题')  # 图片显示的名字
plt.imshow(wc)
plt.axis('off')  # 关闭坐标
plt.show()