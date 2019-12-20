from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv
import numpy as np
import traceback
from selenium.common.exceptions import WebDriverException

# 爬取歌曲详细信息的爬虫


def get_song_detail(url, driver):
    driver.get(url)
    # 切换到内容的iframe
    driver.switch_to.frame("contentFrame")

    # 定位到标题
    title_song = driver.find_element_by_css_selector("em.f-ff2").text

    # 获取歌手和专辑名
    name_artist = driver.find_element_by_css_selector("p.des.s-fc4>span").get_attribute("title")
    name_album = driver.find_element_by_css_selector("p.des.s-fc4>a").text

    # 定位到歌词元素

    # 定位到展开按钮
    # btn_more = driver.find_element_by_css_selector("a#flag_ctrl")
    # btn_more = driver.find_element_by_css_selector("div.crl")

    ele_lyric = driver.find_element_by_css_selector("div#lyric-content")
    # content_lyric = ele_lyric.text[0:-2:1]  # 获取歌词
    content_lyric = ele_lyric.get_attribute('textContent')  # 获取歌词
    # btn_more.click()  # 点击一下展开按钮
    # content_lyric_more = driver.find_element_by_css_selector("div#flag_more").get_attribute('textContent')[0:-2:1]
    # content_lyric = content_lyric + content_lyric_more  # 拼接字符串
    if len(content_lyric) < 20:  # 歌词长度小于阈值的认定为无效歌词
        content_lyric = ""  # 空串
    else:
        # content_lyric = content_lyric[0:-2:1].replace(',', ' ')  # 先去结尾两个字符再替换文中的逗号
        content_lyric = content_lyric.replace(',', ' ')  # 替换文中的逗号为空格

    number_comments = driver.find_element_by_css_selector("span.sub.s-fc3>span").text


    # 返回一个tuple
    return title_song, name_artist, name_album, number_comments, content_lyric



def main():
    # 网址
    # url = "https://music.163.com/#/song?id=1340128424"  # 这首歌词爬不到?
    # url = "https://music.163.com/song?id=456175021"  # 纯音乐, 没歌词的, 测试
    # url = "https://music.163.com/#/song?id=569214247"
    url = "https://music.163.com/#/song?id=1390625483"

    # 选项
    options = Options()  # 调用sele库进行设置
    options.add_argument("--headless")
    # options.headless = True

    # 传入设置, 创建一个driver
    driver = webdriver.Firefox(options=options,
                               executable_path=r"D:\Files\Library_development\geckodriver-v0.26.0-win64\geckodriver.exe")
    print("<DONE> driver created")

    try:
        detail = get_song_detail(url, driver)
        print(detail)
    except WebDriverException as wde:
        print("<ExceptionOccurred> ", wde.args)
        print("=====")
        print(traceback.format_exc())  # 打印详细信息



    # 关闭驱动, 这点很重要, 不然火狐的进程是不会死的
    driver.close()


if __name__ == '__main__':
    main()




