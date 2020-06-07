import jieba as jb


def jiebaCut():
    generator = jb.cut("这只是一个分词测试Demo", cut_all=False)
    print("/".join(generator))

    jb.add_word("分词测试")
    generator = jb.cut("这只是一个分词测试Demo", cut_all=False)
    print("/".join(generator))

    jb.del_word("分词测试")


def maxMatch():
    print(1)


if __name__ == '__main__':
    jiebaCut()
