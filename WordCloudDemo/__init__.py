from WordCloudDemo.WordCloud import WordCloud
from WordCloudDemo.WordCount import WordStatistic


def generateWCloud():
    ws = WordStatistic("../Resources/comment_1.csv")
    counter = ws.count()
    filtered = ws.filterStopwords(counter, "../Resources/stopwords.txt")

    wc = WordCloud(filtered)
    wc.drawCloud("../Resources/stopwords.txt")


if __name__ == '__main__':
    generateWCloud()