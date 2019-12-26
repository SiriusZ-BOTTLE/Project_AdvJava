import pandas as pd

df = pd.read_csv("../../CSV/评论分词/word_vec.csv",engine='python')
for i in df:
    x=i.split(" ")
    temp=df[i]
    df[i]=x+","
    for j in range(1,len(x)):
        df[i]=df[i]+" "+x[j]
pd.DataFrame(df).to_csv("../../CSV/评论分词/word_vec.txt", header=['64383','128'],index=False, encoding='utf-8')
