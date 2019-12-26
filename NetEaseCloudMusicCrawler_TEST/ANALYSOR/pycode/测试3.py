# load the trained word2vec model
import gensim.models

inpath = '../../CSV/评论分词/model'
model = gensim.models.Word2Vec.load(inpath)

# start with the IMDB data
import re
from nltk.corpus import stopwords
from sklearn.linear_model import SGDClassifier
import pyprind
import numpy as np
import matplotlib.pyplot as plt

stop = stopwords.words('english')
# BatchNum*BatchSize must smaller than 50000
BatchSize = 1000

def tokenizer(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text.lower())
    text = re.sub('[\W]+', ' ', text.lower()) +\
        ' '.join(emoticons).replace('-', '')
    tokenized = [w for w in text.split() if w not in stop]
    return tokenized


def stream_docs(path):
    with open(path, 'r') as csv:
        next(csv)  # skip header
        for line in csv:
            text, label = line[4:-3], int(line[-2])
            text = re.sub('[\'\"\[\]\d\b]','',text)
            while text[0] == ',':
                    text = text[1:]
            yield text.split(', '), label


def get_minibatch(doc_stream, size):
    docs, y = [], []
    try:
        for _ in range(size):
            text, label = next(doc_stream)
            docs.append(text)
            y.append(label)
    except StopIteration:
        return None, None
    return docs, y


clf = SGDClassifier(loss='log', random_state=1, n_iter=1)
ACC = []
 
classes = np.array([0, 1])
pbar = pyprind.ProgBar(21)

for BatchNum in range(25,46): 
    doc_stream = stream_docs(path='movie_data.csv') 
    for _ in range(BatchNum):
        X_train = []
        X_raw, y_train = get_minibatch(doc_stream, size=BatchSize)
        if not X_raw:
            break
        for line in X_raw:
            wordAveVec = np.zeros([100])
            abandon = 0
            try:
                for word in line:
                    wordAveVec = wordAveVec + model[word]
            except KeyError:
                abandon+=1
            wordAveVec = wordAveVec/(len(line) - abandon)
            X_train.append(wordAveVec)    
        clf.partial_fit(X_train, y_train, classes=classes)        
    
    X_raw_test, y_test = get_minibatch(doc_stream, size=(50000-BatchNum*BatchSize))
    X_test = []
    for line in X_raw_test:
            wordAveVec = np.zeros([100])
            abandon = 0
            try:
                for word in line:
                    wordAveVec = wordAveVec + model[word]
            except KeyError:
                abandon+=1
            wordAveVec = wordAveVec/(len(line) - abandon)
            X_test.append(wordAveVec)
    ACC.append(clf.score(X_test,y_test))
    pbar.update()
x = range(25,46)
plt.plot(x, ACC)
plt.xlabel('BatchNum')
plt.ylabel('Accuracy')
plt.grid()
plt.show()    
