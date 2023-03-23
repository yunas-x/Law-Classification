import pathlib
from typing import Union
from docx import Document

async def readSavedDocx(path: pathlib.Path) -> Union[bool, str]: 
    """Reads all paras from saved doc

    Args:
        path (pathlib.Path): path to the file

    Returns:
        Union[bool, str]: false if file is not docx, otherwise inner text
    """
    
    if path.suffix != '.docx':
        return False
    
    doc = Document(path)
    txt = ""
    for para in doc.paragraphs:
        txt += para.text
        
    return txt