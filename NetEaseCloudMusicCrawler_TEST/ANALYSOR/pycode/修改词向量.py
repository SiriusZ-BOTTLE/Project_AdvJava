import pandas as pd

df = pd.read_csv("../../CSV/评论分词/word_vec.csv",engine='python')
for i in df:
    x=i.split(" ")
    temp=df[i]
    print(df[i])
    df[i]=x+","
    for j in range(1,len(x)):
        df[i]=df[i]+" "+x[j]
pd.DataFrame(df).to_csv("../../CSV/评论分词/word_vec_new.csv", header=['64380','128'],index=False, encoding='utf-8')
