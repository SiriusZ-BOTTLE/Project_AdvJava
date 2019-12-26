

import pandas as pd
import numpy as np
import re

from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.faker import Collector, Faker
from pyecharts.charts import Page, WordCloud, Bar, Line

from jieba import analyse



# 文件路径
filePath_allKeyWords = "../../CSV/list_allWords.csv"
filePath_allLyrics = "../../CSV/list_lyric_p.csv"
filePath_singer_sorted = "../../CSV/list_singer_sorted.csv"
filePath_keyWords = "../../CSV/list_keyWords.csv"


v1 = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
v2 = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
v3 = [2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2]


# 读取数据
def read_data():

    # 读取全部的词信息
    list_all_w = np.ravel(np.array(pd.read_csv(filePath_allKeyWords).astype(str))).tolist()

    list_singer_sorted = pd.read_csv(filePath_singer_sorted)
    # list_singer_sorted.iloc[:, 1] = list_singer_sorted.iloc[:, 1].astype("int")
    # list_singer_sorted.iloc[:, 2] = list_singer_sorted.iloc[:, 2].astype("int")

    list_singer_sorted = (np.array(list_singer_sorted)[::-1, :])

    # 读取歌词信息
    list_lyrics = pd.read_csv(filePath_allLyrics)
    list_lyrics = list_lyrics.astype({'歌词': 'str'})
    print(list_lyrics)
    str_lyrics = "".join(np.ravel(np.array(list_lyrics)).tolist())



    keyWords = pd.read_csv(filePath_keyWords, header=None)
    keyWords = (np.array(keyWords)).tolist()

    return list_all_w, list_singer_sorted, str_lyrics, keyWords




def wordCloud_0(words, title):
    wc = WordCloud()
    wc.add("", words, word_size_range=[20, 100])
    wc.set_global_opts(title_opts=opts.TitleOpts(title=title))
    return wc



def bar_0(title, list_itemName, list_className, list_itemValue) -> Bar:
    bar0 = Bar()

    bar0.add_xaxis(list_itemName)
    bar0.add_yaxis(list_className[1], list_itemValue[1])
    bar0.extend_axis(
        yaxis=opts.AxisOpts()
    )

    # bar0.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    bar0.set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-20)),
            datazoom_opts=opts.DataZoomOpts(),
            # legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_right="%2"),
      )

    line = Line()
    line.add_xaxis(list_itemName)
    line.add_yaxis(list_className[0], list_itemValue[0], yaxis_index=1, areastyle_opts=opts.AreaStyleOpts(opacity=0.2))
    line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    bar0.overlap(line)

    return bar0


def overlap_bar_line() -> Bar:
    bar = (
        Bar()
            .add_xaxis(Faker.months)
            .add_yaxis("蒸发量", v1)
            .add_yaxis("降水量", v2)
            .extend_axis(
            yaxis=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"), interval=5
            )
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Overlap-bar+line"),
            datazoom_opts=opts.DataZoomOpts(),
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(formatter="{value} ml")
            ),
        )
    )

    line = Line().add_xaxis(Faker.months).add_yaxis("平均温度", v3, yaxis_index=1, areastyle_opts=opts.AreaStyleOpts(opacity= 0.9))
    bar.overlap(line)
    return bar


def main():

    list_all_words, list_singer_sorted, str_lyrics, keyWords = read_data()


    print(list_all_words)
    print(list_singer_sorted)
    # 只切前两百个
    list_singer_p = (list_singer_sorted[0:200:1, [0, 2]]).tolist()



    wc_0 = wordCloud_0(list_singer_p, "最热歌手一览")

    # 只切前300个
    list_itemName = (np.ravel(list_singer_sorted[0:300:1, [0]])).tolist()
    list_value = (list_singer_sorted[0:300:1, [2, 1]]).transpose().tolist()
    print(type(list_value[0]))

    print(len(list_value[0]))
    print(len(list_value[1]))
    print(list_itemName)
    bar = bar_0("综合排序", list_itemName, ["歌手热度", "歌曲数量"], list_value)
    # bar = overlap_bar_line()


    print(str_lyrics)

    keyWords_chinese = keyWords[0:100:1]
    keyWords_eng = keyWords[100:200:1]

    wc_1 = wordCloud_0(keyWords_chinese, "中文歌词热词")
    wc_2 = wordCloud_0(keyWords_eng, "英文歌词热词")

    page = Page()
    page.add(wc_0)
    page.add(bar)
    page.add(wc_1)
    page.add(wc_2)


    # page.render()

    page.render(r"./wordCloud.html")

    print(list_singer_p)

    pass


if __name__ == '__main__':
    main()








