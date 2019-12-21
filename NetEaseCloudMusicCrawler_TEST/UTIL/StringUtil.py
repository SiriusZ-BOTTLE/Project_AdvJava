import difflib


# 字符串相似度比较函数, 传入两个字符串
def get_sim(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()















