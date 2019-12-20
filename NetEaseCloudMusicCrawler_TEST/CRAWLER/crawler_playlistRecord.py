from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv
import pandas as pd






def get_playlist_records(url, driver, max_size):
    count_page = 0
    list_playlist_records = []
    # 一页一页解析
    while url != 'javascript:void(0)' and count_page < max_size:
        print("<PageCount> ", count_page)
        print("<URL> ", url)

        # 用WebDriver加载页面
        driver.get(url)
        # 切换到内容的iframe
        driver.switch_to.frame("contentFrame")  # 这个可以在浏览器里面观察到得到

        # 找到需要的内容
        # m-pl-container是歌单项容器对象的id
        data = driver.find_element_by_id("m-pl-container") \
            .find_elements_by_tag_name("li")  # "li"是歌单项的名称
        # 这里有一个坑点, 敲函数的时候误将"find_elements_by_tag_name"敲成了"find_element_by_tag_name"
        # 这样的花就只拿到了一个元素....底下就出异常了....草, 有点坑

        print(data)

        # 解析一页中的所有歌单
        for count_playlist in range(len(data)):
            # 获取播放数, 可以用XPATH://span[@class='nb']
            playNum = data[count_playlist].find_element_by_class_name("nb").text  # "nb"是播放数对象的类名
            mask = data[count_playlist].find_element_by_css_selector("a.msk")
            author = data[count_playlist].find_element_by_css_selector("a.nm")

            title_playlist = mask.get_attribute("title")
            link_playlist = mask.get_attribute("href")
            name_author = author.get_attribute("title")
            link_author = author.get_attribute("href")
            # 写入到文件
            # writer.writerow(
            #     [mask.get_attribute("title"),
            #      playNum,
            #      mask.get_attribute("href"),
            #      author.get_attribute("title"),
            #      author.get_attribute("href")]
            # )

            list_playlist_records.append((title_playlist, playNum, link_playlist, name_author, link_author))
            print(count_playlist, title_playlist, playNum, link_playlist, name_author, link_author)

        # 定位下一页的url
        url = driver.find_element_by_css_selector("a.zbtn.znxt").get_attribute("href")

        count_page = count_page + 1
    return list_playlist_records



# 主函数
def main():
    # 网址
    url = "https://music.163.com/" \
          "#/discover/playlist/" \
          "?order=hot&cat=%E5%85%A8%E9%83%A8&limit=20&offset=0"

    # 选项
    options = Options()  # 调用sele库进行设置
    options.add_argument("--headless")
    # options.headless = True

    # 传入设置, 创建一个driver
    driver = webdriver.Firefox(options=options, \
                               executable_path= \
                                   r"D:\Files\Library_development\geckodriver-v0.26.0-win64\geckodriver.exe")
    print("<DONE> driver created")

    # 存储歌单的csv文件(追加模式,'\n'换行避免空行)
    # file_csv = open("list_playlist_records.csv", "a", encoding='utf-8')
    # writer = csv.writer(file_csv, lineterminator='\n')

    list_playlist_records = []
    # 抓取100个歌单
    try:
        list_playlist_records = get_playlist_records(url, driver, 5)
    except WebDriverException as wde:
        print("<ExceptionOccurred> ", wde.args)
        print("=====")
        print(traceback.format_exc())  # 打印详细信息

    pd.DataFrame(list_playlist_records).to_csv("list_playlist_records.csv", header=False, index=False ,encoding="utf-8")

    # 关闭驱动
    driver.close()



if __name__ == '__main__':
    main()




