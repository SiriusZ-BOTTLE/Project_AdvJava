import pandas as pd
import csv
import codecs
import numpy

path='E:/Java高级大作业/list_song_details.csv'
author=set()
# result=numpy.zeros(shape=(8116,2),dtype=str)
a=list()
b=list()
c=list()
csv_data = pd.read_csv(path)
csv_data=csv_data.values
for i in range(len(csv_data)):
    if(csv_data[i][1] in author):
        for j in range(len(author)):
            if(a[j]==str(csv_data[i][1])):
                b[j]=str(int(b[j])+1)
                c[j]=str(int(c[j])+int(csv_data[i][3]))
                break
    else:
        a.append(csv_data[i][1])
        b.append(str(1))
        c.append(str(csv_data[i][3]))
        author.add(csv_data[i][1])
d=list(zip(a,b,c))
d=sorted(d, key=lambda d : int(d[1]))
pd.DataFrame(pd.DataFrame(d).to_csv("E:/Java高级大作业/data2-歌曲数量排序.csv", header=['作者','歌曲数','歌曲总评论数'], index=False, encoding='utf-8'))
d=sorted(d,key=lambda d : int(d[2]))
pd.DataFrame(pd.DataFrame(d).to_csv("E:/Java高级大作业/data2-歌手热度排序.csv", header=['作者','歌曲数','歌曲总评论数'], index=False, encoding='utf-8'))
