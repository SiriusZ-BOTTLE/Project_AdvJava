import jieba
import pandas as pd
path='../../CSV/评论分词/'
with open("../../StopWords.txt",encoding="utf-8") as fr:
    stopwords = set([word.strip() for word in fr])
df = pd.read_csv("../../csv/list_comment_details.csv")
df['内容'] = df['内容'].map(lambda x: " ".join([i for i in jieba.cut(str(x)) if i not in stopwords]))

pd.DataFrame(zip(df['内容'],df['热评'])).to_csv("../../CSV/评论分词/评论总分词.csv", header=['内容','热评'], index=False, encoding='utf-8')
