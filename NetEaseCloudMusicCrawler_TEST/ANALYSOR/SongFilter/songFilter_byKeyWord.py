# 根据关键词筛选歌曲

import UTIL.StringUtil as SU
import pandas as pd
import numpy as np


from pyecharts import options as opts
from pyecharts.charts import Bar, Page
from pyecharts.charts import Page, Pie





# 文件路径
filePath_allKeyWords = "../../CSV/list_allWords.csv"
filePath_allLyrics = "../../CSV/list_lyric_p.csv"
filePath_allSongs = "../../CSV/list_song_details.csv"


# 读取数据
def read_data():

    # 读取全部的词信息
    list_all_w = np.ravel(np.array(pd.read_csv(filePath_allKeyWords).astype(str))).tolist()

    # 读取全部歌词(每一行一个字符串)
    list_lyrics = pd.read_csv(filePath_allLyrics)
    list_lyrics = list_lyrics.astype({'歌词': 'str'})

    # 读取全部歌曲信息
    list_songs = pd.read_csv(filePath_allSongs, header=None)
    list_songs = list_songs.values[:, [0]]  # 切片, 只拿取歌名
    list_songs = np.ravel(np.array(list_songs)).tolist()

    list_lyrics = (np.ravel(np.array(list_lyrics))).tolist()
    # print(list_lyrics)
    list_lyrics_p = []
    for i in range(len(list_lyrics)):
        list_words = list_lyrics[i].split(' ')
        list_lyrics_p.append(list_words)  # 分割后添加到处理表

    return list_all_w, list_lyrics_p, list_songs


def bar_0(title, list_itemName, list_className, list_itemValue) -> Bar:
    bar = Bar()
    bar.add_xaxis(list_itemName)

    for i in range(len(list_className)):
        bar.add_yaxis(list_className[i], list_itemValue[i], stack="stack1")
    bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    bar.set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-20)),
            datazoom_opts=opts.DataZoomOpts(),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_right="%2"),
    )
    return bar


def pie_0(list_data0, list_data1) -> Pie:
    pie = Pie()
    # list_data = [list(z) for z in zip(Faker.choose(), Faker.values())]
    # print(list_data)
    pie.add("", list_data0, radius=["60%", "90%"],)
    pie.add("", list_data1, radius=["10%", "30%"], )
    pie.set_global_opts(
            title_opts=opts.TitleOpts(title="关键词百分比环形图"),
            legend_opts=opts.LegendOpts(
                orient="vertical", pos_top="15%", pos_left="2%"
            ),
        )
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    return pie







def main():

    print("<Initializing>")

    read_data()

    # 读取数据
    list_all, list_lyrics, list_songs = read_data()

    # 总歌曲数量
    num_song = len(list_lyrics)
    print("<AllSong> ", num_song)

    # print(np.array(list_lyrics))

    # 获取输入
    line = input("Please Enter The Key Word:\n")
    # 拆分关键词
    list_kw = line.split(';')

    # 输出关键词
    print("<KeyWords> ", list_kw)


    # 处理后列表
    list_kw_p = []

    len_all_kw = len(list_all)

    # 针对每一个给定的关键词, 从词库中找到最接近的词语
    for i in range(len(list_kw)):
        max_sim = 0.0
        index_max = 0
        for j in range(len_all_kw):
            sim_tmp = SU.get_sim(list_kw[i], list_all[j])
            if max_sim < sim_tmp:
                max_sim = sim_tmp
                index_max = j
        if max_sim >= 0.1:
            list_kw_p.append(list_all[index_max])  # 用词库中接近的词替换

    # 去除重复
    list_kw_p = list(set(list_kw_p))

    print("<KeyWords> ", list_kw_p)

    if len(list_kw_p) ==0:
        print("无法检索到对应的关键词")
        return  # 退出

    # 匹配度列表
    list_matchCount = []

    # list_componentCount = []

    count_records = 0
    count_allWords = 0
    for i in range(num_song):
        count_tmp = 0
        count_component = [0] * len(list_kw_p)  # 分量计数
        count_allWords = count_allWords + len(list_lyrics[i])
        for j in range(len(list_kw_p)):
            num = list_lyrics[i].count(list_kw_p[j])
            count_tmp = count_tmp + num
            count_component[j] = count_component[j] + num  # 分量计数+1

        if count_tmp != 0 and count_records < 200:  # 只添加有匹配度的
            list_matchCount.append([i, count_tmp, list_songs[i], count_component])
            count_records = count_records + 1

    print(list_matchCount)

    # 降序排序
    list_matchCount = sorted(list_matchCount, key=lambda list_matchCount : int(list_matchCount[1]), reverse=True)

    print(list_matchCount)

    list_itemName = (np.ravel(np.array(list_matchCount)[:, 2:3])).tolist()
    print(list_itemName)

    # 这两句真的是写吐血了....
    list_itemValues = np.array((np.ravel(np.array(list_matchCount)[:, 3:4])).tolist())
    list_itemValues = list_itemValues.transpose().tolist()
    list_className = list_kw_p


    data_pie_0 = []


    count_keyWords = 0
    for i in range(len(list_kw_p)):
        count_tmp = int(np.sum(list_itemValues[i]))
        count_keyWords = count_keyWords + count_tmp
        data_pie_0.append([list_kw_p[i], count_tmp])
    print(data_pie_0)

    data_pie_1 = [['关键词', count_keyWords], ["其他", count_allWords - count_keyWords]]

    page = Page()

    chart0 = bar_0(line + " 关键词检索", list_itemName, list_className, list_itemValues)
    page.add(chart0)

    chart1 = pie_0(data_pie_0, data_pie_1)
    page.add(chart1)

    page.render()  # 渲染页面


if __name__ == '__main__':
    main()

# 生命;意义;力量;价值;疯狂;酒;欲望;生活
