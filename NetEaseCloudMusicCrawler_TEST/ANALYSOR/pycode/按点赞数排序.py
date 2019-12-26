import pandas as pd

path='../../CSV/list_comment_details.csv'
#数据列索引
columns=['歌名','作者','专辑','评论数','歌词']
# csv_data = np.loadtxt(path, dtype=str,delimiter=',',encoding='utf-8')
csv_data = pd.read_csv(path)
csv_data=csv_data.values
print(csv_data)
csv_data=sorted(csv_data, key=lambda csv_data : int(csv_data[3]))
# csv_data.to_csv('E:/Java高级大作业/data1', header=True, index=False)
pd.DataFrame(csv_data).to_csv("E:/Java高级大作业/GitHub项目/Project_AdvJava/NetEaseCloudMusicCrawler_TEST/CSV/data1.csv", header=['歌名','作者','专辑','评论数','歌词'], index=False, encoding='utf-8')

print("保存文件成功，处理结束")
