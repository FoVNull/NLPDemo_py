import re


class ChineseFilter:
    @staticmethod
    def filterText(s: str) -> list:
        texts = [u"啊a1446呃呃OK⭕🎶步品破茶",
                 u"点击http://www.hikki.top网址",
                 u"链接ed2k://|file|dld-021.avi|1016078437|620703E6CD6F00BF67102544D6BB00C4|/",
                 u"啊啊啊✨ ​​​好🌹",
                 s]
        pattern = re.compile(r"[^\x00-\xff\u200b]", )
        emojiPattern = re.compile(r"[\u4e00-\u9fa5]", )
        res = []
        for text in texts:
            temp = pattern.findall(text)# 筛选掉单个的16进制字符
            textWithEmoji = ""
            for i in temp: textWithEmoji += i

            chinese = ""
            for i in emojiPattern.findall(textWithEmoji): chinese += i

            # 如果没其他语言的话，emojiPattern.split(textWithEmoji)也可以
            textEmoji = ""
            for i in re.findall("[^\u4e00-\u9fa5ぁ-んァ-ン]", textWithEmoji): textEmoji += i

            jp=""
            for i in re.findall("[ぁ-んァ-ン]", textWithEmoji): jp +=i

            dic = {"text": chinese, "emoji": textEmoji}
            if jp !="" : dic["others"] = jp

            res.append(dic)
        return res
