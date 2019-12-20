# 获取全部歌曲的详细信息

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv
import pandas as pd
import numpy as np
import traceback
import time


from selenium.common.exceptions import WebDriverException


# 爬取歌曲链接中首页的评论信息
def get_comment_under_song(url, driver):
    driver.get(url)
    # 切换到内容的iframe
    driver.switch_to.frame("contentFrame")

    # time.sleep(0.05)

    # ele_comments = driver.find_element_by_css_selector("div.cmmts.j-flag")
    # 找到全部评论元素
    # eles = driver.find_elements_by_css_selector("div.cmmts.j-flag>*")

    list = []
    eles = driver.find_elements_by_xpath("//div[@class='cmmts j-flag']/*")
    count_try = 0

    while len(eles) <= 1 and count_try < 100:  # 只重试100次
        print("页面未完全加载")
        if len(eles) == 0 and count_try >= 10:
            print("超过10次无法加载, 可能评论信息不存在")
            break  # 不再尝试
        time.sleep(0.1)  # 等待0.1秒
        eles = driver.find_elements_by_xpath("//div[@class='cmmts j-flag']/*")
        count_try = count_try + 1


    if len(eles) <= 1:
        print("页面无法加载或没有评论")

    # 完整的第一条评论的点赞数路径
    # "//div[@class='cmmts j-flag']/*[2]//div[@class='rp']/a[1]"

    popular = 0
    # count = 1  # xpath从1开始计数...

    comment = ""
    print("<EleNum> ", len(eles))
    for i in range(len(eles)):
        if eles[i].tag_name == "div":  # 评论元素

            # 获取评论内容
            comment = driver.find_element_by_xpath("//div[@class='cmmts j-flag']/*[%d]//div[@class='cnt f-brk']" % (i+1)).text
            comment = comment.replace(',', ' ')
            comment = comment.replace('\n', ' ')
            # 获取点赞数
            num_likes = driver.find_element_by_xpath("//div[@class='cmmts j-flag']/*[%d]//div[@class='rp']/a[1]" % (i+1)).text[1:-1:1]

            # count = count + 1
            # 转换为int
            if len(num_likes) != 0:
                if num_likes.endswith("万"):
                    num_likes = int(float(num_likes[0:-1:1]) * 10000)  # 切片去除汉字, 转为float并乘以10000
                else:
                    num_likes = int(num_likes)
            else:
                num_likes = 0  # 无点赞

            list.append((num_likes, popular, comment))  # 添加到列表

        elif eles[i].tag_name == "h3":  # 边界元素
            if eles[i].text.startswith("精彩"):
                popular = 1  # 激活热评标记
            elif eles[i].text.startswith("最新"):
                popular = 0
        else:  # 是br元素(换行), 不管它
            pass

    return list


def main():
    # 网址
    # url = "https://music.163.com/playlist?id=3077285212"

    # url = "https://music.163.com/#/song?id=411214279"  # 雅俗共赏 OK
    # url = "https://music.163.com/#/song?id=1345865324"  # 不知名的歌 OK
    url = "https://music.163.com/#/song?id=1357704311"  # 炸了

    # 选项
    options = Options()  # 调用sele库进行设置
    options.add_argument("--headless")
    # options.headless = True

    # 传入设置, 创建一个driver
    driver = webdriver.Firefox(options=options,
                               executable_path=r"D:\Files\Library_development\geckodriver-v0.26.0-win64\geckodriver.exe")
    print("<DONE> driver created")

    # 存储歌单的csv文件(追加模式,'\n'换行避免空行)
    # file_csv = open("test.csv", "w", encoding='utf-8')
    # writer = csv.writer(file_csv, lineterminator='\n')

    # writer.writerow(["标题", ""])
    try:
        comment_list = get_comment_under_song(url, driver)
        print(comment_list)
    except WebDriverException as wde:
        print("<ExceptionOccurred> ", wde.args)
        print("=====")
        print(traceback.format_exc())  # 打印详细信息



    # 关闭驱动, 这点很重要, 不然火狐的进程是不会死的
    driver.close()


if __name__ == '__main__':
    main()




