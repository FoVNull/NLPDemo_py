from Cleaning.ChineseDemo import ChineseFilter
from Cleaning.EnglishDemo import EnglishFilter
from Cleaning.TextSpider import TextSpider
from Cleaning.Languages import Languages
from Cleaning.SplitProcessor import SplitProcessor

if __name__ == '__main__':
    tweet = TextSpider.getText()
    ChRes = ChineseFilter.filterText(tweet)
    processor = SplitProcessor(Languages.Others, ChRes)
    # EnRes = EnglishFilter.filterText("tweet")
    # processor = SplitProcessor(Languages.English, EnRes)
    # processor.restoreToStem()
    # processor.spaCyRestore()
    processor.chineseSplit()



