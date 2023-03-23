from tempfile import NamedTemporaryFile
import pathlib
import shutil

import os

from fastapi import UploadFile

async def saveDocx(file: UploadFile) -> pathlib.Path:
    """Saves uploaded docx file on the computer with new cyphered name

    Args:
        file (UploadFile): File uploaded via http

    Returns:
        pathlib.Path: Path to the file assigned by system
    """
    
    try:
        suffix = pathlib.Path(file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = pathlib.Path(tmp.name)
    finally:
        file.file.close()
    return tmp_path

async def turnToDocx(path: pathlib.Path) -> pathlib.Path:
    """Turns file to docx format (if it is not) via changing it's extention

    Args:
        path (pathlib.Path): path to the file

    Returns:
        pathlib.Path: new path
    """
    
    if (path.exists() and path.suffix != '.docx'):
        path = path.rename(str(path.absolute().resolve()) + '.docx')
    
    return path
