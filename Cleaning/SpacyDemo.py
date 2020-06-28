import en_core_web_sm
import spacy
import ja_core_news_sm
import ginza

from WordCloudDemo import WordStatistic


class SpacyProcessor:
    def __init__(self, contents: list):
        self.contents = []
        for i in contents: self.contents.append(i["text"])

    def spaCyRestore(self):
        nlp = en_core_web_sm.load()
        print(type(nlp))
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

    def japaneseSplit(self):
        # https://www.kaggle.com/lazon282/japanese-stop-words
        # stopSets = WordStatistic.generateStopSets("../Resources/japanese-stopwords.txt")

        # nlp: ginza.Japanese = spacy.load('ja_ginza')  # ginza的model
        nlp: ginza.Japanese = ja_core_news_sm.load()

        # 自定义停用词
        # ginza.STOP_WORDS.add("かっこ")

        # nlp.pipe()为generator，利用yield doc缓存执行doc的生成，效率比逐个生成doc高
        for doc in nlp.pipe(self.contents):
            for token in doc:
                if not nlp.vocab[token.text].is_stop:
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

            # 输出名词
            # for none in doc.noun_chunks:
                # print(none)

            # 识别实体
            # for entity in doc.ents:
                # print(entity.text, entity.label_)
