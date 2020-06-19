import re


class EnglishFilter:
    @staticmethod
    def filterText(s: str) -> list:
        texts = [u"Checkmate other youtube musicians... oh wait",
                 u"nevermind thought it was 90m, but he'll catch up soon :D",
                 u"check it on https://www.youtube.com/Davie504 OMG😀",
                 u"the proxy url is SOCKS5://127.0.0.1:Port Check it👈",
                 s]
        res = []
        for text in texts:
            filteredText = ""
            for i in re.split("[\w]+://[^\s]*", text):
                for j in re.findall("[\x00-\x2F\x3A-\xff]", i): filteredText += j

            emoji = ""
            for i in re.findall("[^\x00-\xff\u200b\u4e00-\u9fa5ぁ-んァ-ン]", text): emoji += i

            urls = ""
            for i in re.findall("[\w]+://[^\s]*", text): urls += i

            res.append({"text": filteredText, "emoji": emoji, "urls": urls})
        return res
