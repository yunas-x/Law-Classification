from pandas import read_csv
import pathlib

from docx2python import docx2python

import pathlib
from typing import List

import re

import pandas as pd


escapes = ''.join([chr(char) for char in range(1, 32)])
translator = str.maketrans('', '', escapes)

def get_paragraphs(content, 
                   paragraphs: List):
    
    if type(content) == list:
        if len(content) != 0: 
            for i in content:
                get_paragraphs(i, paragraphs)
    else:
        if '----' not in content:
            content = content.translate(translator)
            if len(content) > 0:
                paragraphs.append(content)
        

def readSavedDocm(path: pathlib.Path): 
    """Reads all paras from saved doc

    Args:
        path (pathlib.Path): path to the file

    Returns:
        Union[bool, str]: false if file is not docx, otherwise inner text
    """
    
    try:
        with docx2python(path, extract_image=False) as doc_context:
            txt = doc_context.body_runs
    
    except:
        txt = []
        
    return txt

def getDocmFilesTexts(path_from: pathlib.Path, ext: str) -> List:
    
    pattern = f'**/*{ext}'
    
    texts = []
    paths = []
    
    for dir in path_from.glob(pattern):
        if '.versions' in str(dir):
            continue
        texts.append(readSavedDocm(dir))
        paths.append(dir.stem)
    
    print(texts)
    
    return texts, paths
    
def get_data(txt):
    if len(txt) > 0:
        paragraphs = []
        
        get_paragraphs(txt, paragraphs)

        
    else:
        paragraphs = []
              
    return paragraphs

from dateutil.parser import parse

def get_info(paras: List):
    name = ''
    date = ''
    num = ''            
    for i, s in enumerate(paras):
        if re.sub(' +', ' ', s).upper() == "ПОСТАНОВЛЕНИЕ":

            for j in range (i+1, i+6):
                w = paras[j]
                if len(w.strip()) == 10 and '.' in w:
                    date = w.strip()
                elif w.strip() == "№":
                    num = paras[j+1].strip()
                elif name == '' and (len(w) > 10 or date != '' and len(w) > 6):
                    name = w.replace("«", '"').replace("»", '"').strip()
                    
    return name, date, num
                       
from_test = pathlib.Path(r"C:\Users\yunas\OneDrive\Рабочий стол\postanovlenie")

df_path = r"C:\Users\yunas\OneDrive\Рабочий стол\CourseWork\Analysis\expdata2.csv"

df = read_csv(df_path, delimiter=";", encoding='Windows-1251', encoding_errors="ignore")

df = df[df["actkind"] == 'Постановление']


texts, paths = getDocmFilesTexts(from_test, ".docm")

names = []
contents = []
categories = []

unrequited = []

for p, t in zip(paths, texts):
    try:
        paras = get_data(t)
        name, d, num = get_info(paras)
        
        vals = df[(df['shortcontent'] == name)]
        
        if (vals.shape[0] > 1 and num != ''):
            vals = vals[vals['regnumber'].str.contains(num)]

        
        if (vals.shape[0] > 1 and d != ''):
            vals = vals[vals['regdate'].str.contains(d)]
        
        if (vals.shape[0] == 1):
            names.append(name)
            contents.append(" ".join(paras))
            categories.append(vals["acttheme"].values.tolist()[0])
        
    except:
        print('error')


data = {'file': names,
        'content': contents,
        'category': categories}

df_ = pd.DataFrame(data)

df_.to_csv(r'C:\Users\yunas\OneDrive\Рабочий стол\zakon1.csv')

