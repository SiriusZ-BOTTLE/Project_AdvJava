import math
import numpy
import pandas as pd

path='../../CSV/歌词分词/总分词.csv'
df = pd.read_csv(path)
df=df.values
result=set()
for i in range(len(df)):
    if (df[i][0]==df[i][0])==False:
        continue
    else:
        str_list=''.join(df[i]).split()
        for j in range(len(str_list)):
            result.add(str_list[j])
b=numpy.array(list(result)).reshape(len(result),1)
pd.DataFrame(b).to_csv("../../CSV/歌词分词/去重分词.csv", header=['词'], index=False, encoding='utf-8')
