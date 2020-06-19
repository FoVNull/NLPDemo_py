from Cleaning.ChineseDemo import ChineseFilter
from Cleaning.EnglishDemo import EnglishFilter
from Cleaning.TextSpider import TextSpider

if __name__ == '__main__':
    tweet = TextSpider.getText()
    # res1 = ChineseFilter.filterText(tweet)
    res2 = EnglishFilter.filterText(tweet)
    for i in res2:print(i)
