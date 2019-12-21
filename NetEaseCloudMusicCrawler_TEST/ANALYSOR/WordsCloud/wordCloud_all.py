from pyecharts import options as opts

import pandas as pd
import numpy as np

from pyecharts.commons.utils import JsCode
from pyecharts.faker import Collector, Faker
from pyecharts.globals import ThemeType
from pyecharts.charts import Page, WordCloud



# 文件路径
filePath_allKeyWords = "../../CSV/list_keyWords_all.csv"

# 读取数据
def read_data():

    # 读取全部的关键词信息
    list_all_w = np.ravel(np.array(pd.read_csv(filePath_allKeyWords).astype(str))).tolist()


    return list_all_w




def wordCloud_0(words, title):
    wc = WordCloud()
    wc.add("", words, word_size_range=[20, 100])
    wc.set_global_opts(title_opts=opts.TitleOpts(title= title))
    return wc




def main():

    list_all_words = read_data()



    pass





if __name__ == '__main__':
    main()








