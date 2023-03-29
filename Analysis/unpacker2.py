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
    
    return texts, paths
    
def get_data(txt):
    if len(txt) > 0:
        name = ""
        paragraphs = []
        get_paragraphs(txt, paragraphs)
            
        for i in range(10):
            if re.sub(' +', ' ', paragraphs[i]).upper() == "ЗАКОН ПЕРМСКОГО КРАЯ":
                name = paragraphs[i+1].replace("«", '"').replace("»", '"')
                break
        
    else:
        print("empty")
        name = ""
        paragraphs = []
              
    return paragraphs, name
                        
from_test = pathlib.Path(r"C:\Users\yunas\OneDrive\Рабочий стол\2014\12")
from_zakon = pathlib.Path(r"C:\Users\yunas\OneDrive\Рабочий стол\zakon")

df_path = r"C:\Users\yunas\OneDrive\Рабочий стол\CourseWork\Analysis\expdata2.csv"

df = read_csv(df_path, delimiter=";", encoding='Windows-1251', encoding_errors="ignore")

df = df[df["actkind"] == 'Закон']


texts, paths = getDocmFilesTexts(from_zakon, ".docx")
names = []
contents = []
categories = []

unrequited = []
    
for p, t in zip(paths, texts):
    try:
        paras, name = get_data(t)
        
        if '_' in p:
        
            a, b = p.split('_')
            b = b.split('.')
            b = '-'.join(b[::-1])

        else:
            a = ''
            b = ''
        
        vals = df[(df['shortcontent'] == name)]
        if (vals.shape[0] > 1 and a != ''):
            vals = vals[(df['formnamesed'].str.contains(a) & df['formnamesed'].str.contains(b))]
        
        if (vals.shape[0] == 0):
            unrequited.append(name)

        if (vals.shape[0] == 1):
            names.append(name)
            contents.append(" ".join(paras))
            categories.append(vals["acttheme"].values.tolist()[0])
        
        
    except:
        print('error')

data = {'file': names,
        'content': contents,
        'category': categories}

data2 = {'file': unrequited}

df_ = pd.DataFrame(data)

df_.to_csv(r'C:\Users\yunas\OneDrive\Рабочий стол\post.csv')

df_2 = pd.DataFrame(data2)

df_2.to_csv(r'C:\Users\yunas\OneDrive\Рабочий стол\zakon2222.csv')
