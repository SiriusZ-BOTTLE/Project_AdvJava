import re
import pandas as pd
import numpy as np

from jieba import analyse


filePath_allLyrics = "../../CSV/list_lyric_p.csv"
filePath_output = "../../CSV/list_keyWords.csv"

num_key = 100

def main():
    # 读取歌词信息
    list_lyrics = pd.read_csv(filePath_allLyrics)
    list_lyrics = list_lyrics.astype({'歌词': 'str'})
    list_lyrics = np.ravel(np.array(list_lyrics)).tolist()

    str_lyrics = "".join(list_lyrics)

    print(str_lyrics[0])

    # 去除英文字符
    str_chinese = re.sub("([a-zA-Z])+", "", str_lyrics)
    # 去除中文字符
    str_eng = re.sub("([\u4e00-\u9fa5]+)", "", str_lyrics)


    # 抽取100个关键词
    keyWords_chinese = analyse.extract_tags(str_chinese, topK=num_key)
    print(keyWords_chinese)
    keyWords_eng = analyse.extract_tags(str_eng, topK=num_key)
    print(keyWords_eng)


    # 合并关键词
    list_all = []
    list_all.extend(keyWords_chinese)
    list_all.extend(keyWords_eng)

    print(list_all)

    list_count = [0] * (2 * num_key)

    for i in range(2 * num_key):
        list_count[i] = str_lyrics.count(list_all[i])


    data = [list_all, list_count]

    print(data)

    pd.DataFrame(data).transpose().to_csv(filePath_output, header=None, index=False)


    pass




if __name__ == '__main__':
    main()






