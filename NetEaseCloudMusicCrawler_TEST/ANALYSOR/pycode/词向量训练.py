import pandas as pd
import gensim


if __name__ == '__main__':
    # 词向量训练
    df = pd.read_csv("../../CSV/评论分词/评论总分词.csv", header=None)
    sentences = df.iloc[:, 0].astype("str").map(lambda x: x.split(" "))
    model = gensim.models.Word2Vec(sentences, size=128, workers=4, min_count=0)
    model.wv.save_word2vec_format('../../CSV/评论分词/word_vec.txt', binary=False)
