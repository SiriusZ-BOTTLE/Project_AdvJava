import jieba
import pandas as pd
path='../../CSV/歌词分词/'
# stopwords = {}.fromkeys([ line.rstrip() for line in open('../../StopWords.txt') ])
with open("../../StopWords.txt",encoding="utf-8") as fr:
    stopwords = set([word.strip() for word in fr])
print(stopwords)
df = pd.read_csv("../../csv/list_song_details.csv")
# csv_data=csv_data.values
# df=df.values
df['歌词'] = df['歌词'].map(lambda x: " ".join([i for i in jieba.cut(str(x)) if i not in stopwords]))

# for i in range(len(df)):
#     pd.DataFrame(pd.DataFrame(jieba.cut(str(df[i][4])))).to_csv("E:/Java高级大作业/歌词分词/%06d" % (i) +".csv", header=['歌词'], index=False, encoding='utf-8')
pd.DataFrame(df['歌词']).to_csv("../../CSV/歌词分词/总分词.csv", header=['歌词'], index=False, encoding='utf-8')


# seg_list = jieba.cut("我来到北京清华大学", cut_all=True)#
# print ("Full Mode: " + "/ ".join(seg_list))#全模式
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# print("Default Mode: " + "/ ".join(seg_list))#精确模式
#
# seg_list = jieba.cut("他来到了网易杭研大厦")#默认是精确模式
# print(", ".join(seg_list))
#
# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")#搜索引擎模式
# print(", ".join(seg_list))
