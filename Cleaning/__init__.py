from Cleaning.ChineseDemo import ChineseFilter
from Cleaning.EnglishDemo import EnglishFilter
from Cleaning.JapaneseDemo import JapaneseFilter
from Cleaning.SpacyDemo import SpacyProcessor
from Cleaning.TextSpider import TextSpider
from Cleaning.Languages import Languages
from Cleaning.SplitProcessor import SplitProcessor

if __name__ == '__main__':
    # tweet = TextSpider.getText()

    # chRes = ChineseFilter.filterText(tweet)
    # processor = SplitProcessor(Languages.Others, chRes)
    # processor.chineseSplit()

    # enRes = EnglishFilter.filterText("tweet")
    # syProcessor = SpacyProcessor(enRes, Languages.English)
    # processor = SplitProcessor(Languages.English, EnRes)
    # processor.restoreToStem()
    # syProcessor.englishRestore()

    jpRes = JapaneseFilter.filterText("これの産地はアメリカのテキサスです")
    syProcessor = SpacyProcessor(jpRes, Languages.Japanese)
    syProcessor.wordVector()



