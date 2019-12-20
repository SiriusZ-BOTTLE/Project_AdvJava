from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv
import numpy as np
import traceback
from selenium.common.exceptions import WebDriverException





# 解析页面中的全部歌曲, URL是歌单的链接
def get_song_records(url, driver):
    driver.get(url)
    # 切换到内容的iframe
    driver.switch_to.frame("contentFrame")

    # 找到需要的内容

    # 定位歌曲记录的容器, 容器标签为"tbody"
    # container = driver.find_element_by_tag_name("tbody")
    # 找到全部的记录项目
    records = driver.find_elements_by_xpath("//tbody/tr");

    list = []

    for i in range(len(records)):
        # 调用css定位器
        # song = records[i].find_element_by_css_selector("span.txt>a")
        # 用XPath的话, "//"表示任意级, "/"表示一级
        # 也可以用这个函数, 效果没差: .find_element_by_css_selector("//span[@class='txt']/a")

        link_song = song.get_attribute("href")
        title_song = records[i].find_element_by_css_selector("span.txt>a>b").get_attribute("title")

        title_song = title_song.replace(' ', ' ')  # 去除奸奇空格, 替换为普通空格
        author = records[i].find_element_by_css_selector("div.text").get_attribute("title")

        print(i, title_song, link_song, author)
        # print(i)

        list.append((title_song, link_song, author))
    # return np.array(list)
    return list



def main():
    # 网址
    # url = "https://music.163.com/playlist?id=3077285212"

    url = "https://music.163.com/#/playlist?id=2476409230"

    # 选项
    options = Options()  # 调用sele库进行设置
    options.add_argument("--headless")
    # options.headless = True

    # 传入设置, 创建一个driver
    driver = webdriver.Firefox(options=options,
                               executable_path=r"D:\Files\Library_development\geckodriver-v0.26.0-win64\geckodriver.exe")
    print("<DONE> driver created")

    # 存储歌单的csv文件(追加模式,'\n'换行避免空行)
    file_csv = open("test.csv", "w", encoding='utf-8')
    writer = csv.writer(file_csv, lineterminator='\n')

    # writer.writerow(["标题", ""])
    list = []
    try:
        list = get_song_records(url, driver)
    except WebDriverException as wde:
        print("<ExceptionOccurred> ", wde.args)
        print("=====")
        print(traceback.format_exc())  # 打印详细信息

    print(list)

    # 关闭驱动, 这点很重要, 不然火狐的进程是不会死的
    driver.close()


if __name__ == '__main__':
    main()



