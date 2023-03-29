import numpy as np
import pandas as pd
from pandas import read_csv

import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from sklearn.linear_model import LogisticRegression
import re
from bs4 import BeautifulSoup
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]"')
BAD_SYMBOLS_RE = re.compile('[^а-яa-zё #+_]')
STOPWORDS = set(stopwords.words('russian'))
STOPWORDS.add("проект")
STOPWORDS.add('субъект права')
STOPWORDS.add('рег')
STOPWORDS.add('номер')
STOPWORDS.add('№')
STOPWORDS.add('дата')

filename = r'C:\Users\yunas\OneDrive\Рабочий стол\CourseWork\classifier.joblib.pkl'

from pathlib import Path

class ClassifierWrapper():
    
    model = False
    
    def __init__(self, force_refit=False):
        

        
        if ClassifierWrapper.model == False:
            pass
        else:
            self = model
            return
        
        path = Path(__file__).parent
        df = read_csv(r'C:\Users\yunas\OneDrive\Рабочий стол\CourseWork\zakon1.csv')
        df1 = read_csv(r'C:\Users\yunas\OneDrive\Рабочий стол\CourseWork\zakon.csv')
        df2 = pd.concat([df, df1])
        df2['content1'] = df2['content'].apply(ClassifierWrapper.clean_text)
        
        self.df = df2
        
        if force_refit:
            try:
                self.load()
                return
            except:
                print("No saved model")
        
        self.model = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                   ('scale', StandardScaler(with_mean=False)),
                ('clf', LogisticRegression(n_jobs=1, class_weight='balanced', C=1e3))])
        
        X = self.df.content1
        y = self.df.category
        self.model.fit(X, y)
        
        self.persist()
        
        model = self

    def persist(self):
        joblib.dump(self.model, filename, compress=2)
        
    def load(self):
        self.model = joblib.load(filename)
    
        

    @staticmethod
    def clean_text(text):
        """
            text: a string
            
            return: modified initial string
        """
        text = BeautifulSoup(text, "lxml").text # HTML decoding
        text = text.lower() # lowercase text
        text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
        text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
        text = ' '.join(word for i, word in enumerate(text.split()) if word not in STOPWORDS) # delete stopwors from text
        return text



if __name__ == "__main__":
    a = ClassifierWrapper()

    txt = "Звоним узнать, купили ли мегаускоритель частиц"
    txt = ClassifierWrapper.clean_text(text=txt)
    data = [ClassifierWrapper.clean_text(txt)]

    arr = np.asarray(data)

    df1 = pd.DataFrame({"x": data})

    print(df1)

    pred = a.model.predict(df1["x"])
    print(pred[0])


