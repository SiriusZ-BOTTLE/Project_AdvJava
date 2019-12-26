import pandas as pd
import numpy as np
df = pd.read_csv('../../CSV/评论分词/word_vec.csv', encoding='utf-8')
df=df.values
result=[]

for i in range(len(df)):
    x= str(df[i])[3:-2].split(' ')  # 分割，并生成新列print(df)
    result.append(x)
np.set_printoptions(linewidth=100)
pd.set_option('display.width', 1000)

ar=np.array(result)
# print(zip(ar[:,0],ar[:,1:]))
pd.DataFrame(list(zip(ar[:,0],ar[:,1:]))).to_csv("../../CSV/评论分词/word_vec_new.csv", header=['64380','128'], index=False, encoding='utf-8')
