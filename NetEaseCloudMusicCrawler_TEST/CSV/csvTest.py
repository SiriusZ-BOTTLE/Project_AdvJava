import pandas as pd
import numpy as np

filePath_keyWords = "./list_keyWords.csv"

keyWords = pd.read_csv(filePath_keyWords, header=None)
keyWords = ((np.array(keyWords))).tolist()

print(keyWords)























