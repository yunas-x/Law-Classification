from datetime import datetime
from fastapi import Depends, Request, Response, UploadFile, FastAPI
from fastapi.responses import FileResponse

from ReadNSave.ReadSavedFile import readSavedDocx
from ReadNSave.FileSave import saveDocx, turnToDocx

from DBManagement.DBContext import SessionLocal

from sqlalchemy.orm import Session

from DAO.incoming_dao import addIncoming
from DAO.classified_dao import addClassified

from DBManagement.Incomming.incoming_pydantic_model import document_model
from DBManagement.Classified.classified_pydantic_model import classified_model

from Fill_Classifier import filename


app = FastAPI(title="Document Classifier")

def get_db(request: Request):
    return request.state.db

@app.middleware("http")
async def db_session_middleware(request: Request, 
                                call_next
                               ):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

@app.get("/", 
         status_code=200, 
         summary="Returns a system description"
        )
async def description():
    return  {
                "author": "yunas",
                "tested on": "HP 250 G7 Notebook PC",
                "RAM": 8,
                "CPU": "Intel Core i5-1035G1 CPU",
                "Frequency": "1 GHz",
                "Server": "uvicorn",
            }

@app.get("/help", 
         status_code=200, 
         summary="Returns classification"
        )
async def classes():
    return FileResponse(filename)

@app.post("/classify", 
          description="Saves the document and reads it "
          + "if done successfully checks its length, and if enough data "
          + "returns a class type of the document",
          summary="Takes a docx file and classifies it according the classifier",
          response_description="A JSON response in format {'doc': logged_doc, 'classid': ID, 'class': classified}, " +
          "where doc is a filename in the system, ID is id for a class, and class is the type of the document"
         )
async def classify(file: UploadFile, 
                   db: Session = Depends(get_db)
                  ):
    
    """Takes uploaded file, saves it to the disk then tries to read it.
       If done successfuly classfies the file
    
    Args:
        file (UploadFile): File uploaded by http
        db (Session, optional): DB session to log operations. Defaults to Depends(get_db).

    Returns:
        _type_: {'doc': logged_doc, 'classid': ID, 'class': classified} response
    """
    
    path = await saveDocx(file)
    path = await turnToDocx(path)
    

    incoming_doc_log = document_model(name=str(path.absolute()), recieved_on=datetime.utcnow())
    logged_doc = addIncoming(db=db, item=incoming_doc_log)
    
    txt = await readSavedDocx(path)
    
    if txt:
        id = 1
        classified = "Success"
    else:
        id = 0
        classified = "Not a docx, reformat file"
    
    ### classified
    
    #classified_log = classified_model(id=logged_doc.id, result=logged_doc.name)
    #classified = addClassified(db=db, item=classified_log)

    return {'doc': logged_doc, 'class_id': id, 'class': classified}
