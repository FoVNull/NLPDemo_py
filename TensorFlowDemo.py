import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json
import matplotlib.pyplot as plt
import numpy as np


def tokenizerTest():  # tokenizer测试
    sentences = ["I love my dog",
                 "I love my cat",
                 "You love my dog!",
                 "Do you think my dog is amazing?"]

    # tokenizer = Tokenizer(num_words=100)
    """
    使用Out of Vocabulary,可以使未在字典中的词统一分类为OOV
    否则sequence中不显示该词
    """
    tokenizer = Tokenizer(num_words=100, oov_token="<OOV>")
    tokenizer.fit_on_texts(sentences)  # 构建字典

    word_index = tokenizer.word_index
    print(word_index)

    seq = tokenizer.texts_to_sequences(sentences)
    print(seq)

    """
    test_sen = ["I got a dog"]
    seq_t = tokenizer.texts_to_sequences(test_sen)
    print(seq_t)
    """

    # post会将填充的0移到后面
    # maxlen设定最长的长度，truncating设置裁剪超出长度的list时是从前还是从后
    padded = pad_sequences(seq, padding="post", maxlen=5, truncating="post")
    print(padded)


""" 调整json格式 (如果需要的话...>_<)
def standardizeJSON():
    data = "{"
    with open("Resources/test.json", "r") as f:
        for i in f.readlines():
            data += str(i.strip() + "," + "\n")

    with open("Resources/test.json", "w") as f:
        f.write(data+"}")
"""


def plot_graphs(history, string):
    plt.plot(history.history[string])
    plt.plot(history.history['val_' + string])
    plt.xlabel("Epochs")
    plt.ylabel(string)
    plt.legend([string, 'val_' + string])
    plt.show()


def modelTraining():  # 模型训练测试
    data = []
    with open("Resources/test.json", "r") as f:
        for line in f:
            data.append(json.loads(line))

    sentences = [];labels = [];urls = []
    for item in data:
        sentences.append(item["headline"])
        labels.append(item["is_sarcastic"])
        urls.append(item["article_link"])

    tokenizer = Tokenizer(oov_token="<OOV>")
    tokenizer.fit_on_texts(sentences)

    maxLen = 100
    # 区分训练和测试数据
    seq_train = tokenizer.texts_to_sequences(sentences[0:20000])
    padded_train = pad_sequences(seq_train, padding="post", maxlen=maxLen)
    labels_train = labels[0:20000]

    seq_test = tokenizer.texts_to_sequences(sentences[20000:])
    padded_test = pad_sequences(seq_test, padding="post", maxlen=maxLen)
    labels_test = labels[20000:]

    padded_train = np.array(padded_train)
    labels_train = np.array(labels_train)
    padded_train = np.array(padded_train)
    labels_test = np.array(labels_test)

    embedding_dim = 16
    vocab_size = 30000
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=maxLen),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(24, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.summary()

    num_epochs = 30
    history = model.fit(padded_train, labels_train, epochs=num_epochs,
                        validation_data=(padded_test, labels_test), verbose=2)

    # 模型准确度
    # plot_graphs(history, "accuracy")
    # plot_graphs(history, "loss")

    discernHeadline(model, tokenizer)


def discernHeadline(model: tf.keras.Sequential, tokenizer: Tokenizer):
    # 预测一个实例
    headline = ["granny starting to fear spiders in the garden might be real",
                "teh weather today is bright and sunny"]

    seq = tokenizer.texts_to_sequences(headline)
    padded = pad_sequences(seq, maxlen=100, padding="post", truncating="post")

    print(model.predict(padded))


if __name__ == '__main__':
    # print(tf.__version__)
    # tokenizerTest()
    # standardizeJSON()
    # dataset: https://www.kaggle.com/rmisra/news-headlines-dataset-for-sarcasm-detection
    modelTraining()
