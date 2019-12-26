from collections import defaultdict

import jieba
import gensim
import numpy as np
# import keras
import tensorflow as tf
# from train import build_model, build_embeddings_matrix
# from text_preprocessing import load_stop_words

def load_stop_words():
    """加载停用词"""
    with open("../../StopWords.txt",encoding='utf-8') as fr:
        stop_words = set([word.strip() for word in fr])
    return stop_words

# 建立词索引
def build_embeddings_matrix(word_vec_model):
    # 初始化词向量矩阵
    embeddings_matrix = np.random.random((len(word_vec_model.wv.vocab)+1, 128))
    # 初始化词索引字典
    word_index = defaultdict(dict)

    for index, word in enumerate(word_vec_model.index2word):
        word_index[word] = index + 1
        # 预留0行给查不到的词
        # print(word,word_index)
        # embeddings_matrix[index+1] = word_vec_model.get_vector(word)
    return word_index, embeddings_matrix
# 构建模型
def build_model(word_index, embeddings_matrix):
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Embedding(input_dim=len(word_index)+1,output_dim=128,weights=[embeddings_matrix],input_length=20,trainable=False))
    model.add(tf.keras.layers.GlobalAveragePooling1D())
    model.add(tf.keras.layers.Dense(32, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(1, activation=tf.nn.sigmoid))

    model.compile(optimizer=tf.train.AdamOptimizer(),loss='binary_crossentropy',metrics=['accuracy'])
    model.summary()
    return model

def pred(text):
    word_vec_model = gensim.models.KeyedVectors.load_word2vec_format("../../CSV/评论分词/word_vec.csv", binary=False)
    word_index, embeddings_matrix = build_embeddings_matrix(word_vec_model)
    model = build_model(word_index, embeddings_matrix)
    model.load_weights("../../CSV/model/评论model")

    stop_words = load_stop_words()

    # while True:
        # text = input("请输入一句话：")
    text = [word_index.get(word, 0) for word in jieba.cut(text)]
    text = tf.keras.preprocessing.sequence.pad_sequences([text], maxlen=20, padding='post', truncating='post', dtype="float32")

    res = model.predict(text)[0][0]
    return res*100
    # if res >= 0.5:
    #     print(f"热评, 得分: {res*100}")
    # else:
    #     print(f"低分，得分: {res*100}")


