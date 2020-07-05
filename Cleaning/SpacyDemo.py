import en_core_web_sm
import spacy
import ja_core_news_sm
import ja_core_news_md
import ja_core_news_lg
import ginza
import chakin
from gensim.models import KeyedVectors

from Cleaning import Languages
from WordCloudDemo import WordStatistic


class SpacyProcessor:
    def __init__(self, contents: list, language: Languages):
        self.contents = []
        for i in contents: self.contents.append(i["text"])

        if language.value == "japanese":
            # self.nlp: ginza.Japanese = spacy.load('ja_ginza')  # ginza的model
            self.nlp: ginza.Japanese = ja_core_news_lg.load()

        if language.value == "english":
            self.nlp = en_core_web_sm.load()

    def englishRestore(self):
        for text in self.contents:
            doc = self.nlp(text)

            # nlp.vocab[token]中需要str而非spacy.tokens.token.Token，所以新建一个list
            word_list = []
            for token in doc:
                word_list.append(token.text)

            filtered = ""
            for word in word_list:
                filteredWord = self.nlp.vocab[word]
                if not filteredWord.is_stop: filtered += filteredWord.text+" "

            lemma_word = []
            doc = self.nlp(filtered)
            for token in doc:
                lemma_word.append(token.lemma_)
            # -PRON-是代词符号
            print(lemma_word)

    def japaneseSplit(self):
        # https://www.kaggle.com/lazon282/japanese-stop-words
        # stopSets = WordStatistic.generateStopSets("../Resources/japanese-stopwords.txt")

        # 自定义停用词
        # ginza.STOP_WORDS.add("かっこ")

        # nlp.pipe()为generator，利用yield doc缓存执行doc的生成，效率比逐个生成doc高
        for doc in self.nlp.pipe(self.contents):
            for token in doc:
                if not self.nlp.vocab[token.text].is_stop:
                    info = [
                        token.i,  # トークン番号
                        token.text,  # テキスト
                        token._.reading,  # 読みカナ
                        token.lemma_,  # 基本形
                        token.pos_,  # 品詞
                        token.tag_,  # 品詞詳細
                        token._.inf  # 活用情報
                    ]
                    print(info)

            # 查阅词性简写的意义
            # print(spacy.explain("PROPN"))

            # 输出名词
            # for none in doc.noun_chunks:
                # print(none)

    def splitEntity(self):
        for doc in self.nlp.pipe(self.contents):
            print(doc.text)
            # 识别实体
            for entity in doc.ents:
                print(entity.text, entity.label_)
            print("-----")

    def showVector(self):
        for doc in self.nlp.pipe(self.contents):
            for token in doc:
                if not self.nlp.vocab[token.text].is_stop:
                    print(token.text, token.vector)

    def wordVector(self):
        # 查看词向量
        self.showVector()

        '''
        我们还使用不同模型的词向量来训练，除了以上两种，还可以利用chakin下载
        (github.com/chakki-works/chakin)
        首先查看可下载的日语vectors
        chakin.search(lang='Japanese')
        下载facebook的fastText模型的vectors (github.com/facebookresearch/fastText/)
        chakin.download(number=6, save_dir='./')
        chakin和浏览器下载没区别，太慢了...我直接用迅雷下github上的资源

        我们可以先比较一下各模型的词向量规模以及维度(small版没词向量)
        print("ja_core_news_lg:", ja_core_news_lg.load().vocab.vectors.shape)
        print("ja_core_news_md:", ja_core_news_md.load().vocab.vectors.shape)
        print("ja_ginza:", spacy.load('ja_ginza').vocab.vectors.shape)

        ja_core_news_lg: (480443, 300)
        ja_core_news_md: (20000, 300)
        ja_ginza: (117951, 100)

        fastText替换lg之后的词向量的规模和维度↓
        fastText(ja) :(2319001, 300)

        结论:选用fastText理论上最好

        我们要用它的话，可以直接下载fastText模型(4.2GB...)
        或者替换当前模型的vectors(单下载vectors只有1.2GB)
        '''
        # from gensim.models import KeyedVectors
        # ftv = KeyedVectors.load_word2vec_format('D:/python/myLibs/cc.ja.300.vec.gz', binary=False)
        # self.nlp.vocab.reset_vectors(width=ftv.vectors.shape[1])
        # for word in ftv.vocab.keys():
        #     self.nlp.vocab.set_vector(word, ftv[word])
        # print(self.nlp.vocab.vectors.shape)
        # self.showVector()

