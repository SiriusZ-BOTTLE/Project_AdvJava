# 获取歌单文件中的歌单下的全部歌曲记录

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv
import pandas as pd
import numpy as np
import traceback

import CRAWLER.crawler_songRecord as tool
from selenium.common.exceptions import WebDriverException


filename_playlist = "list_playlist_records.csv"


# 从歌单记录文件中获取全部歌单链接
def get_all_playlist_link_from_playlist_record_file():
    # 文件没有表头, 需要指定"header=None"
    df = pd.read_csv(filename_playlist, header=None)
    records = df.values[:, [2]]  # 切片, 只拿取链接
    return np.ravel(records).tolist()


# main函数
def main():
    # 选项
    options = Options()  # 调用sele库进行设置
    options.add_argument("--headless")
    # options.headless = True

    # 传入设置, 创建一个driver
    driver = webdriver.Firefox(options=options,
                               executable_path=r"D:\Files\Library_development\geckodriver-v0.26.0-win64\geckodriver.exe")
    print("<DONE> driver created")

    list_links_playlist = get_all_playlist_link_from_playlist_record_file()

    # 去除重复歌单
    # list_links_playlist = np.unique(list_links_playlist).tolist()  # 取消, 歌单应该不会重复
    list_song_records = []

    # 逐个遍历歌单链接, 拿取歌单中所有的歌曲
    count = 0
    max_size = 101
    count_song = 0
    while count < len(list_links_playlist) and count < max_size:
        try:
            print(list_links_playlist[count])
            list_tmp = tool.get_song_records(list_links_playlist[count], driver)


        except WebDriverException as wde:
            print("<ExceptionOccurred> ", wde.args)
            print("=====")
            print(traceback.format_exc())  # 打印详细信息
        else:
            count_song = count_song + len(list_tmp)
            list_song_records.extend(list_tmp)
            print("<PlayListCount> ", count)
            print("<SongCount> ", count_song)

        count = count + 1
        # 每5个清空缓存
        if count % 5 == 0:
            driver.refresh()
            driver.delete_all_cookies()
            print("<Done> refresh")



    # 去除重复歌曲
    # list_song_records = np.unique(list_song_records)  # 这招不管用, np太垃圾了
    list_song_records = list(set(list_song_records))  # 这招管用但是顺序会乱, 但是无所谓啦
    # print(list_song_records)
    pd.DataFrame(list_song_records).to_csv("list_song_records_2.csv", header=False, index=False, encoding='utf-8')

    # 关闭驱动
    driver.close()
    pass



if __name__ == '__main__':
    main()













