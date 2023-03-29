import pathlib
from typing import List, Union
from docx import Document
from docx2python import docx2python

escapes = ''.join([chr(char) for char in range(1, 32)])
translator = str.maketrans('', '', escapes)


async def readSavedDocx(path: pathlib.Path) -> Union[bool, str]: 
    """Reads all paras from saved doc

    Args:
        path (pathlib.Path): path to the file

    Returns:
        Union[bool, str]: false if file is not docx, otherwise inner text
    """
    
    txt_body = read(path)
    paras = get_data(txt_body)
    text = ' '.join(paras)
    return text

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
        

def read(path: pathlib.Path): 
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

def get_data(txt):
    if len(txt) > 0:
        paragraphs = []
        
        get_paragraphs(txt, paragraphs)

        
    else:
        paragraphs = []
              
    return paragraphs


