import sys
from collections import defaultdict

import jieba
import gensim
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split


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

# 生成三组数据集
def train_data(word_index):
    df = pd.read_csv("../../CSV/评论分词/评论总分词.csv",header=0,names=["review", "label"],engine='python',encoding='utf-8')
    # print(df['review'])
    df["word_index"] = df["review"].astype("str").map(lambda x: np.array([word_index.get(i, 0) for i in x.split(" ")]))
    print(df["word_index"])
    # 填充及截断
    train = tf.keras.preprocessing.sequence.pad_sequences(df["word_index"].values, maxlen=20, padding='post', truncating='post', dtype="float32")
    # print(train)
    # print(df['label'])
    x_train, x_test, y_train, y_test = train_test_split(train, df['label'], test_size=0.2, random_state=1)

    # 从训练集上分出验证集
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.15)
    return x_train, x_val, x_test, y_train, y_val, y_test


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
# 读取数据
word_vec_model = gensim.models.KeyedVectors.load_word2vec_format("../../CSV/评论分词/word_vec.csv",binary=False)
# 建立词索引
word_index, embeddings_matrix=build_embeddings_matrix(word_vec_model)
x_train, x_val, x_test, y_train, y_val, y_test=train_data(word_index)
# print(x_train)
# print(x_val)
# print(x_test)
model=build_model(word_index, embeddings_matrix)
# 训练
model.fit(x_train, y_train, epochs=100, validation_data=(x_val, y_val))

# 评估
results = model.evaluate(x_test, y_test)
print(f"损失: {results[0]}, 准确率: {results[1]}")

# 模型保存
model.save_weights('../../CSV/model/评论model')
