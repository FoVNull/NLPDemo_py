from Cleaning.Languages import Languages
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import en_core_web_sm
import jieba

from WordCloudDemo import WordStatistic


class SplitProcessor:
    def __init__(self, language: Languages, contents: list):
        self.language = language.value
        self.contents = []
        for i in contents: self.contents.append(i["text"])

    def restoreToStem(self):
        stop_words = set(stopwords.words(self.language))

        for text in self.contents:
            tokens = word_tokenize(text)  # 分词
            texts = []
            for i in tokens:
                if i not in stop_words: texts.append(i)

            stems = []
            ps = PorterStemmer()
            wordnet_lemmatizer = WordNetLemmatizer()
            for word in texts:
                rootWord = ps.stem(word)  # 获取词根
                stems.append(rootWord)
            print(stems)

            lemma_word = []
            for w in texts:  # 还原成原型
                word1 = wordnet_lemmatizer.lemmatize(w, pos="n")
                word2 = wordnet_lemmatizer.lemmatize(word1, pos="v")
                word3 = wordnet_lemmatizer.lemmatize(word2, pos=("a"))
                lemma_word.append(word3)
            print(lemma_word)

    def spaCyRestore(self):
        nlp = en_core_web_sm.load()
        for text in self.contents:
            doc = nlp(text)

            # nlp.vocab[token]中需要str而非spacy.tokens.token.Token，所以新建一个list
            word_list = []
            for token in doc:
                word_list.append(token.text)

            filtered = ""
            for word in word_list:
                filteredWord = nlp.vocab[word]
                if not filteredWord.is_stop: filtered += filteredWord.text+" "

            lemma_word = []
            doc = nlp(filtered)
            for token in doc:
                lemma_word.append(token.lemma_)
            # -PRON-是代词符号
            print(lemma_word)

    def chineseSplit(self):
        stopSets = WordStatistic.generateStopSets("../Resources/HIT_stopwords.txt")
        stopSets.add("啊啊啊")

        wordList = []
        jieba.add_word("步品破茶")
        for text in self.contents:
            generator = jieba.cut(text, cut_all=True)
            for i in generator:
                if i not in stopSets: wordList.append(i)
        # filtered = filter(lambda i: i not in stopSets, wordList)
        print(wordList)