import jieba as jb
import pandas as pd
import collections


class WordStatistic:
    def __init__(self, path):
        self.df = pd.read_csv(path)

    def count(self) -> collections.Counter:
        """
        hashMap = {}
        for i in wordList:
            if not hashMap.__contains__(i): hashMap.setdefault(i, 0)
            hashMap[i] += 1
        x = sorted(hashMap.items(), key=lambda e: e[1], reverse=True)
        """
        wordList = self.cutWord()
        wordCounts = collections.Counter(wordList)
        return wordCounts

    def cutWord(self) -> list:
        wordList = []
        for index, row in self.df.iterrows():
            generator = jb.cut(row[6], cut_all=True)
            for i in generator: wordList.append(i)
        return wordList

    def filterStopwords(self, counter: collections.Counter, stopListPath: str) -> collections.Counter:
        wordList = []
        for i in counter.elements(): wordList.append(i)

        stopSets = self.generateStopSets(stopListPath)
        filterRes = filter(lambda i: not stopSets.__contains__(i) and i != '' and i != ' ', wordList)

        return collections.Counter(filterRes)

    @staticmethod
    def generateStopSets(path) -> set:
        stopSets = set()
        with open(path, 'r', encoding='utf8') as file:
            strs = file.readlines()
            for s in strs: stopSets.add(s.strip())
        return stopSets
