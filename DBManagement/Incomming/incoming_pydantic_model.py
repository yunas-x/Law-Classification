from datetime import datetime
from pydantic import BaseModel

class document_model(BaseModel):
    name: str
    recieved_on: datetime

class document_model_create(document_model):
    pass

class document_model_recieve(document_model):
    id: int
    
    class Config:
        orm_mode = True
