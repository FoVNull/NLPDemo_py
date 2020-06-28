import re


class JapaneseFilter:
    """
    # ひらがなの抽出
    hiragana = re.findall("[ぁ-ん]", txt)
    # カタカナの抽出
    katakana = re.findall("[ァ-ン]", txt)
    # 漢字の抽出 和中文汉字相同
    kanji = re.findall("[一-龥]", txt)

    包含了日文的特殊符号
    ぁ = \u3041    龥 = \u9fa5
    \u3041-\u9fa5
    """

    @staticmethod
    def filterText(s: str) -> list:
        texts = [u"MVかっこ良過ぎです！明日のライブも凄く楽しみにしてます^_^",
                 u"愛美さん超絶カッコよかったです✨",
                 u"ダウンロードリンクはed2k://|file|dld-021.avi|1016078437|6207|/ チェックしてね",
                 u"代理のホストはSOCKS5://127.0.0.1:Port、ご注意を",
                 u"サイサイとまたコラボしてくれて本当に嬉しいですありがとうございます😭",
                 s]
        res = []
        for text in texts:
            url = ""
            for i in re.findall("[\x00-\xff]+://[\x00-\xff][^\s]*", text): url += i

            emoji = ""
            for i in re.findall("[^\x00-\xff\u200b\u3041-\u9fa5]", text): emoji += i

            jp = ""
            for i in re.findall("[\u3041-\u9fa5]", text):jp += i

            res.append({"text": jp, "url": url, "emoji":emoji})
        return res