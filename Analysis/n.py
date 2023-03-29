from pandas import read_csv
import pathlib

from docx2python import docx2python

import pathlib
from typing import List

import re

import pandas as pd

from_zakon = pathlib.Path(r"C:\Users\yunas\OneDrive\Рабочий стол\Текста")

escapes = ''.join([chr(char) for char in range(1, 32)])
translator = str.maketrans('', '', escapes)

def get_data(txt):
    if len(txt) > 0:
        paragraphs = []
        
        get_paragraphs(txt, paragraphs)

        
    else:
        paragraphs = []
              
    return paragraphs

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

texts, paths = getDocmFilesTexts(from_zakon, ".docx")

contents = []
categories = []


for p, t in zip(paths, texts):
    try:
        paras = get_data(t)
        contents.append(" ".join(paras))
        categories.append("0")
        
    except:
        print('error')


data = {'content': contents,
        'category': categories}

df_ = pd.DataFrame(data)

df_.to_csv(r'C:\Users\yunas\OneDrive\Рабочий стол\nepravo.csv')