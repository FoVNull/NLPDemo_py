from Spider.WordCloud import WordCloud
from Spider.WordCount import WordStatistic

if __name__ == '__main__':
    ws = WordStatistic("../Resources/comment_1.csv")
    counter = ws.count()
    filtered = ws.filterStopwords(counter, "../Resources/stopwords.txt")

    wc = WordCloud(filtered)
    wc.drawCloud("../Resources/stopwords.txt")