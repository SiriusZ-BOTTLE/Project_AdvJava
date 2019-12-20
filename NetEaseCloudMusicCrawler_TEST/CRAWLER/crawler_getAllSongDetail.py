# 获取全部歌曲的详细信息

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv
import pandas as pd
import numpy as np
import traceback

import CRAWLER.crawler_songDetail as tool
from selenium.common.exceptions import WebDriverException


# 歌曲记录文件
filename_playlist = "list_song_records_2.csv"


# 从歌单记录文件中获取全部歌单链接
def get_all_song_link_from_song_records_file():
    # 文件没有表头, 需要指定"header=None"
    df = pd.read_csv(filename_playlist, header=None)
    records = df.values[:, [1]]  # 切片, 只拿取链接
    return np.ravel(records).tolist()




def main():

    # 选项
    options = Options()  # 调用sele库进行设置
    options.add_argument("--headless")
    # options.headless = True

    # 传入设置, 创建一个driver
    driver = webdriver.Firefox(options=options,
                               executable_path=r"D:\Files\Library_development\geckodriver-v0.26.0-win64\geckodriver.exe")
    print("<DONE> driver created")

    list_links_song = get_all_song_link_from_song_records_file()

    # print(list_links_song)

    list_song_details = []
    # 逐个遍历歌曲链接, 爬取歌曲详细信息
    count = 0  # 预先设定从哪里开始爬
    max_size = 20000  # 最终位置

    file_csv = open("list_song_details.csv", "a", encoding='utf-8')
    writer = csv.writer(file_csv, lineterminator='\n')

    while count < len(list_links_song) and count < max_size:
        try:
            # 获取歌曲详细信息
            print(count, list_links_song[count])
            detail = tool.get_song_detail(list_links_song[count], driver)

            # list_song_details .append(detail)
            # print(detail)
            writer.writerow(detail)
        except WebDriverException as wde:
            print("<ExceptionOccurred> ", wde.args)
            print("=====")
            print(traceback.format_exc())  # 打印详细信息

        count = count + 1
        # 每100个刷新缓冲区, 输出到文件, 并且重启驱动
        if count % 100 == 0:
            file_csv.flush()
            driver.close()
            # 传入设置, 创建一个driver
            driver = webdriver.Firefox(options=options,
                                       executable_path=r"D:\Files\Library_development\geckodriver-v0.26.0-win64\geckodriver.exe")
            print("<DONE> driver created")

    # print(list_song_details)
    # pd.DataFrame(list_song_details).to_csv("list_song_details.csv", header=False, index=False)

    # 关闭文件
    file_csv.close()

    # 关闭驱动, 这点很重要, 不然火狐的进程是不会死的
    driver.close()


if __name__ == '__main__':
    main()






